import datetime
import json
from smtplib import SMTPAuthenticationError
import django
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from jwt import ExpiredSignatureError
#from pyee import BaseEventEmitter
#from pymitter import EventEmitter
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
import pdb

from django.core.mail import EmailMultiAlternatives

from Login_Registration_Using_REST_Services.settings import EMAIL_HOST_USER, file_handler
from User.token import token_activation, token_validation

from User.serializers import  UserSerializer, LoginSerializer, ResetSerializer, EmailSerializer
from django.core.validators import validate_email
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
def home(request):
   
    return render(request, 'home.html')

class Registrations(GenericAPIView):

    serializer_class = UserSerializer

    def get(self, request):
         return render(request, 'user/registration.html')

    def post(self, request):
        data=post
        username = request.data['username']
        email = request.data['email']
        password1 = request.data['password1']
        password2 = request.data['password2']

        send_msg = {
            'success': False,
            'message': "not registered yet",
            'data': [],
        }

        try:
            validate_email(email)
        except Exception as e:
            send_msg['message'] = "please enter vaild email address"
            logger.error("error: %s while as email entered was not a vaild email address", str(e))
            return HttpResponse(json.dumps(send_msg), status=400)

        # user input is checked
        if username == "" or email == "" or password1 == "" or password2=="":
            send_msg['message'] = "one of the details missing"
            logger.error("one of the details missing logging in")
            return HttpResponse(json.dumps(send_msg), status=400)

        # if email exists it will show error message
        elif User.objects.filter(email=email).exists():
            send_msg['message'] = "email address is already registered "
            logger.error("email address is already registered  while logging in")
            return HttpResponse(json.dumps(send_msg), status=400)

        else:
            try:
                user_created = User.objects.create_user(username=username, email=email, password1=password1,password2=password2,
                                                        is_active=True)
                user_created.save()

                # user is unique then we will send token to his/her email for validation
                if user_created is not None:
                    token = token_activation(username, password1)
                    url = str(token)
                    surl = get_surl(url)
                   

                    mail_subject = "Activate your account by clicking below link"
                    mail_message = render_to_string('email_validation.html', {
                        'user': user_created.username,
                        'domain': get_current_site(request).domain,
                        'surl': surl
                    })
                    recipient_email = user_created.email
                    email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
                    email.send()
                    send_msg = {
                        'success': True,
                        'message': 'please check the mail and click on the link  for validation',
                        'data': [token],
                    }
                    logger.info("email was sent to %s email address ", username)
                    return HttpResponse(json.dumps(send_msg), status=201)
            except Exception as e:
                send_msg["success"] = False
                send_msg["message"] = "username already taken"
                logger.error("error: %s while loging in ", str(e))
                return HttpResponse(json.dumps(send_msg), status=400)



class Login(GenericAPIView):

    serializer_class = LoginSerializer
    def get(self,request):
        return render(request, 'Login/login.html')
    def post(self, request):
        data=post
        send_msg = {
            'success': False,
            'message': "not logged in ",
            'data': []
        }
        try:
            username = request.data['username']
            password = request.data['password']
            # validation is done
            if username == "" or password == "":
                send_msg['message'] = 'one or more fields is empty'
                return HttpResponse(json.dumps(send_msg), status=400)
            user = auth.authenticate(username=username, password=password)

            # if user is not none then we will generate token
            if user is not None:
                token = token_validation(username, password)

                send_msg = {
                    'success': True,
                    'message': "successfully logged",
                    'data': [token],
                }
                return HttpResponse(json.dumps(send_msg), status=201)
            else:
                send_msg['message'] = 'invaild credentials'
                logger.error("invaild credentials for username: %s ",username)
                return HttpResponse(json.dumps(send_msg), status=400)
        except Exception as e:
            send_msg['message'] = 'invaild credentials'
            logger.error("error: %s while loging in ", str(e))
            return HttpResponse(json.dumps(send_msg), status=400)


class Logout(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
 
        send_msg = {"success": False, "message": "not a vaild user", "data": []}
        try:
            user = request.user
            send_msg = {"success": True, "message": " logged out", "data": []}
            logger.info("%s looged out succesfully ", user)
            return HttpResponse(json.dumps(send_msg), status=200)
        except Exception:
            logger.error("something went wrong while logging out")
            return HttpResponse(json.dumps(send_msg), status=400)

def activate(request, surl):
    try:
        # decode is done for the JWT token where username is fetched

        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then user account willed be activated
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, "your account is active now")
            return redirect('/login')
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/registration')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/api/registration')
    except ExpiredSignatureError:
        messages.info(request, 'activation link expired')
        return redirect('/api/registration')
    except Exception:
        messages.info(request, 'activation link expired')
        return redirect('/api/registration')



class ForgotPassword(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        email = request.data["email"]
        smd = {
            'success': False,
            'message': "not a vaild email ",
            'data': []
        }
        # email validation is done here

        if email == "":
            smd['message'] = 'email field is empty please provide vaild input'
            return HttpResponse(json.dumps(smd), status=400)
        else:
            try:
                validate_email(email)
            except Exception:
                return HttpResponse(json.dumps(smd) ,status=400)
            try:
                user = User.objects.filter(email=email)
                useremail = user.values()[0]["email"]
                username = user.values()[0]["username"]
                id = user.values()[0]["id"]

                #  here user is not none then token is generated
                if useremail is not None:
                    token = token_activation(username, id)
                    url = str(token)
                    surl = get_surl(url)
                    z = surl.split("/")

                    # email is generated  where it is sent the email address entered in the form
                    mail_subject = "Activate your account by clicking below link"
                    mail_message = render_to_string('email_validation.html', {
                        'user': username,
                        'domain': get_current_site(request).domain,
                        'surl': z[2]
                    })
                    recipientemail = email
                    ee.emit('send_email', recipientemail, mail_message)
                    smd = {
                        'success': True,
                        'message': "check email for vaildation ",
                        'data': []
                    }
                    # here email is sent to user
                    return HttpResponse(json.dumps(smd), status=201)
            except Exception as e:
                print(e)
                response['message'] = "something went wrong"
                return HttpResponse(json.dumps(smd), status=400)









class ResetPassword(GenericAPIView):
    serializer_class = ResetSerializer
    def post(self, request, user_reset):
        password = request.data['password']
        send_msg = {
            'success': False,
            'message': 'password reset not done',
            'data': [],
        }
        # password validation is done in this form
        if user_reset is None:
            send_msg['message'] = 'not a vaild user'
            return HttpResponse(json.dumps(send_msg), status=404)

        elif password == "":
            send_msg['message'] = 'one of the fields are empty'
            return HttpResponse(json.dumps(send_msg), status=400)

        elif len(password) <= 4:
            send_msg['message'] = 'password should be 4 or  more than 4 character'
            return HttpResponse(json.dumps(send_msg), status=400)

        else:
            try:
                user = User.objects.get(username=user_reset)
                user.set_password(password)
                # here we will save the user password in the database
                user.save()

                send_msg = {
                    'success': True,
                    'message': 'password reset done',
                    'data': [],
                }
                return HttpResponse(json.dumps(send_msg), status=201)
            except User.DoesNotExist:
                send_msg['message'] = 'not a vaild user '
                return HttpResponse(json.dumps(send_msg), status=400)





