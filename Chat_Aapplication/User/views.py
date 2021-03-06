from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UsersData,LoggedUser
from django.contrib.auth import login, logout
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from .serializers import (RegistrationSerializers,LoginSerializers,ResetSerializers)
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate, get_user_model
from django.views.generic import TemplateView
from User.token import token_activation
from django.contrib.sites.shortcuts import get_current_site
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
User = get_user_model()
import json
from Chat_Aapplication.settings import SECRET_KEY
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout
import jwt
from .redis import Redis
red = Redis()


class Home(TemplateView):
    template_name = 'UserTemplates/home.html'


class welcome(TemplateView):
    template_name = 'UserTemplates/welcome.html'


class Login(GenericAPIView):
#def login(request):
    serializer_class = LoginSerializers
    def get(self,request):
        return render(request, 'UserTemplates/login.html')

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

        # validation is done
        if username == "" or password == "":
            #messages.info(request, "one of the above field is empty")
            return redirect('/login')
        user = auth.authenticate(username=username, password=password)

        # if user is not none then we will generate token and we will store the token in redis data base
        if user is not None:
            data = {
                'username': username,
                'password': password
            }
            # here token is created and data is stored in redis
            token = token_activation(user.username, password)
            red.set(username,token)
            userlist = []
            logged_user = LoggedUser.objects.all().order_by('username')
            
            for i in logged_user:
                if i.username != username:
                    userlist.append(i.username)
            return render(request, 'chat/index.html')
        else:
            return render(request, 'UserTemplates/login.html')



class Registration(GenericAPIView):
    serializer_class = RegistrationSerializers
    def get(self, request):
        return render(request,'UserTemplates/signup.html')
        
    def post(self, request):
        if request.user.is_authenticated:
            
            return HttpResponse("your are already registred,please do login")
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            return HttpResponse("passwords are not matching")
            
        qs_name = User.objects.filter(
            Q(username__iexact=username)
        )
        qs_email = User.objects.filter(
            Q(email__iexact=email)
        )
        if qs_name.exists():
            return HttpResponse("already user id pret with this username ")
            
        elif qs_email.exists():
            return HttpResponse("already user id present with this  email")
            
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.is_active = False
            user.save()

            
            token = token_activation(user.username, password1)

            current_site = get_current_site(request)
            domain = current_site.domain

            url = str(token)

            surl = get_surl(url)

            slug_url = surl.split('/')

            #print(slug_url[2])
            mail_subject = "Click below link for activate your acount"

            message = render_to_string('UserTemplates/account_activation_link.html',{
                'user' : user.username,
                'domain' : domain,
                'surl' : slug_url[2]
            })

            recipients = email

            email = EmailMessage(mail_subject,message,to=[recipients])
            print(message)
            email.send()

            return HttpResponse("Check your mail and activate your accout")



def activate(request,surl):
    try:
        token_object = ShortURL.objects.get(surl=surl)
        token = token_object.lurl
        decode = jwt.decode(token,SECRET_KEY)
        user_name = decode['username']
        user = User.objects.get(username=user_name)
        if user is not None:
            user.is_active = True
            user.save()
            return redirect('/login/')
        else:
            return HttpResponse('Inavalid username and password please register')
    except KeyError:
        return HttpResponse("Key error")


class ForgotPassword(GenericAPIView):

    def get(self,request):
        return render(request,'UserTemplates/forgotpassword.html')

    def post(self,request):
        email = request.POST.get('email')

        try:
            user = User.objects.filter(email=email)
            useremail = user.values()[0]['email']
            username = user.values()[0]["username"]
            id = user.values()[0]["id"]

            if useremail is not None:
                token = token_activation(username,id)

                url = str(token)
                surl = get_surl(url)
                slug_url = surl.split('/')
                mail_subject = "reset your account password by clicking below link"
                mail_message = render_to_string('UserTemplates/reset_password_token_link.html', {
                    'user': username,
                    'domain': get_current_site(request).domain,
                    'surl': slug_url[2]
                })
                print(mail_message)
                recipientemail = useremail
                email = EmailMessage(mail_subject, mail_message, to=[recipientemail])
                email.send()

            return HttpResponse("Check your mail")
        except TypeError:
            print("Type error")


def reset_password(request, surl):
    
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        
        if user is not None:
            return redirect('/resetpassword/' + str(user)+'/')
        else:
            return redirect('/forgotpassword/')
    except KeyError:
        return HttpResponse("Key Error")


class ResetPassword(GenericAPIView):
    # serializer_class = ResetSerializers

    def get(self,request,user_reset):
        return render(request,"UserTemplates/resetpassword.html")
        
    def post(self, request,user_reset):
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirm_password")

        if password == confirmPassword:
    
            try:
                user = User.objects.get(username=user_reset)
                user.set_password(password)
                user.save()
                return redirect('/login/')

            except KeyError:
                return HttpResponse("Key Error")

        else:
            return HttpResponse("Password missmatch")


def logout(request):
    red.delete()
    return render(request, 'UserTemplates/logout.html')


def session(request):
    return render(request, 'UserTemplates/session.html')