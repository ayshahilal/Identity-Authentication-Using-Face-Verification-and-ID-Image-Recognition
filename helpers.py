from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import jwt
from dotenv import load_dotenv

from models import User

load_dotenv()

def create_session(DATABASE_URL):
    engine = create_engine(DATABASE_URL, echo=False, connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def is_login(session, token):
    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        email = decoded['email']
    except: 
        return False

    user = session.query(User).filter_by(email=email).first()
    if user and user.token == token:
        return user
    else:
        return False
