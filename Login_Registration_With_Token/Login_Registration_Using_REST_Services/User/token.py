
import datetime
import pdb

import jwt
import requests
from Login_Registration_Using_REST_Services.settings import SECRET_KEY, AUTH_ENDPOINT


def token_activation(username, password):
    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now()+datetime.timedelta(days=2)
    }
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token


def token_validation(username, password):
    data = {
        'username': username,
        'password': password
    }
    tokson = requests.post(AUTH_ENDPOINT, data=data)
    token = tokson.json()['access']
    return token
