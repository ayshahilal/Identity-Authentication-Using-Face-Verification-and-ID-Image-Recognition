from dotenv import load_dotenv
from flask import make_response
import jwt

from models import User
from helpers import is_login

load_dotenv()

def login_controller(session, request):
    token = request.cookies.get('token')
    user = is_login(session, token)
    if user:
        return user

    try:
        data = request.form
        email = data['email']
        password = data['password']
    except:
        return False

    user = session.query(User).filter_by(email=email, password=password).first()

    if user:
        encoded_jwt = jwt.encode({"email": email}, "secret", algorithm="HS256")
        user.token = encoded_jwt
        session.add(user)
        session.commit()
        return user
    return False