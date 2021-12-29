import os
import datetime
from .login import login_controller
from .id_card import extract
from .face_verification import verify

def verify_controller(session, request):
    user = login_controller(session, request)
    if user:
        data = request.form
        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.tc = data['tc']
        user.birth_date = datetime.datetime.strptime(data['birthdate'], '%Y-%m-%d')
        if data['gender'] == 'male':
            user.gender = False
        else:
            user.gender = True

        user_path = f"users/{user.email}"
        id_card_path = f"{user_path}/id_cards"
        id_card = request.files['id_card']
        if id_card.filename != '':
            id_card.save(f"{id_card_path}/{datetime.datetime.now().timestamp()}.{id_card.filename.split('.')[-1]}")
        session.add(user)
        session.commit()
        resp = match_photos(user.email)
        if resp:
            user.is_verified = True
            session.add(user)
            session.commit()
            return resp
        return False

def match_photos(email):
    user_path = f"users/{email}"
    id_card_path = f"{user_path}/id_cards"
    face_path = f"{user_path}/faces"

    id_card = os.listdir(id_card_path)[-1]
    informations = extract(f"{id_card_path}/{id_card}")
    if not informations:
        return False
    face = os.listdir(face_path)[-1]
    if verify(f"{id_card_path}/{id_card}", f"{face_path}/{face}"):
        return informations
    return False

