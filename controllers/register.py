from dotenv import load_dotenv
from flask import make_response
import jwt

from models import User
from helpers import is_login

load_dotenv()

def register_controller(session, request):
    try:
        data = request.form
        email = data['email']
        name = data['name']
        password = data['password']
        password_confirmation = data['password_confirmation']
    except:
        return 'error', 'form invalid'

    user = session.query(User).filter_by(email=email).first()

    if password != password_confirmation:
        return 'error', 'passwords not match'

    if user:
        return 'error', 'email already exist'
    
    user = User(name=name, email=email, password=password)
    session.add(user)
    session.commit
    return 'success', 'user created'