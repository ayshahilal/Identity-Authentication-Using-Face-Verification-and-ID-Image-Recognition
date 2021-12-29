import os
from flask import Flask, request, redirect, url_for, render_template, make_response
from werkzeug.utils import secure_filename
from matplotlib import pyplot as plt
from controllers import login_controller, register_controller, verify_controller
from binascii import a2b_base64
import cv2
import io
import numpy as np
import datetime

from helpers import create_session

app = Flask(__name__)
app.secret_key = ",123.ke, ;qwek;m "
DATABASE_URL = os.getenv('DATABASE_URL')

session = create_session(DATABASE_URL)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = login_controller(session, request)
    if user:
        response = make_response(redirect(url_for('index')))
        response.set_cookie('token', user.token)
        return response
    if request.method == 'GET':

        return render_template('login.html', message=request.args.get('message', default=None), is_login=False)

    elif request.method == 'POST':
        return render_template('login.html', error='email or password incorrect', code=401, is_login=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', is_login=False)
    elif request.method == 'POST':
        resp = register_controller(session, request)
        if resp[0] == 'error':
            return render_template('register.html', error=resp[1], is_login=False)
        else:
            return redirect(url_for('login', message=resp[1]))

@app.route('/logout', methods=['GET'])
def logout():
    user = login_controller(session, request)
    if user:
        user.token = ""
        session.add(user)
        session.commit()
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie('token', '')
    return resp

@app.route('/setfacephoto', methods=['POST'])
def setfacephoto():
    user = login_controller(session, request)
    if user:
        user_path = f"users/{user.email}"
        face_path = f"{user_path}/faces"
        try:
            os.mkdir(user_path)
        except:
            pass
        try:
            os.mkdir("users")
        except:
            pass
        try:
            try:
                os.mkdir(f"{face_path}")
            except:
                pass
            try:
                os.mkdir(f"{user_path}/id_cards")
            except:
                pass
            os.mkdir(user_path)
        except:
            pass
        if len(os.listdir(face_path)) > 4:
            for filename in os.listdir(face_path):
                os.remove(os.path.join(face_path, filename))

        data = request.json
        image = data['image']
        image = image.split(',', 1)[1]
        image = a2b_base64(image)
        with open(f"{face_path}/{datetime.datetime.now().timestamp()}.png", 'wb') as f:
            f.write(image)

    return "asd"

@app.route('/verify', methods=['POST'])
def verify():
    resp = verify_controller(session, request)
    if resp:
        print(resp)
        return render_template('success.html', informations=resp, is_login=True)
    else:
        return redirect(url_for('index', error='not match'))

@app.route('/', methods=['GET'])
def index():
    user = login_controller(session, request)
    if not user:
        response = make_response(redirect('/login'))
        response.set_cookie('token', '')
        return response
    if user.is_verified:
        return render_template('success.html', is_verified=user.is_verified)
    error = request.args.get('error', default=None)
    return render_template("index.html", is_login=True, is_verified=user.is_verified, error=error)


if __name__ == "__main__":
    app.run()