from datetime import datetime
import jwt
from Chat_Aapplication.settings import SECRET_KEY
AUTH_ENDPOINT = "http://127.0.0.1:8000/auth/jwt/"


def token_activation(username, password):
    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now()+datetime.timedelta(minutes=6)
    }

    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')

    return token


# def token_validation(username, password):

#     data = {
#         'username': username,
#         'password': password
#     }
#     tokson = requests.post(AUTH_ENDPOINT, data=data)
#     token = tokson.json()['access']
#     return token