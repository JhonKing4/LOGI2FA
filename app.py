from flask import Flask, request, jsonify, session
import pyotp
import os
from flask_cors import CORS
from flask_session import Session
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración de Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
Session(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app, supports_credentials=True)

# Configuración de Twilio
TWILIO_ACCOUNT_SID = '11'
TWILIO_AUTH_TOKEN = '111'
TWILIO_PHONE_NUMBER = '111'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Simulación de base de datos
users = {
    'user1': {'password': 'password123', 'email': 'banking415@yahoo.com', 'phone': '+529981454665', '2fa_secret': pyotp.random_base32()}
}

def send_token_sms(phone, secret):
    totp = pyotp.TOTP(secret)
    token = totp.now()
    print(f"Token generado: {token}") 
    message = f'Your 2FA token is: {token}'
    
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    return token

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)

    if user and user['password'] == password:
        session['username'] = username
        session['2fa_secret'] = user['2fa_secret']
        session['2fa'] = False
        token = send_token_sms(user['phone'], user['2fa_secret'])
        session['2fa_token'] = token
        return jsonify({'message': 'Login successful, please check your SMS for the 2FA token.'}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/two-factor', methods=['POST'])
def two_factor():
    if 'username' not in session:
        return jsonify({'message': 'Session expired, please log in again.'}), 401

    data = request.json
    token = data.get('token')
    username = session['username']
    user = users.get(username)

    if '2fa_token' not in session:
        return jsonify({'message': 'No 2FA token found in session.'}), 401

    session_token = session['2fa_token']
    print(f"Token enviado por el cliente: {token}")
    print(f"Token almacenado en la sesión: {session_token}")

    if token != session_token:
        print("Los tokens son diferentes")
        return jsonify({'message': 'Invalid 2FA token'}), 401

    totp = pyotp.TOTP(user['2fa_secret'])
    print(f"Secreto de 2FA del usuario: {user['2fa_secret']}")
    result = totp.verify(token)
    print(f"Resultado de la verificación de TOTP: {result}")

    if result:
        session['2fa'] = True
        return jsonify({'message': '2FA successful'}), 200

    return jsonify({'message': 'Invalid 2FA token'}), 401

@app.route('/api/protected', methods=['GET'])
def protected():
    if 'username' not in session or not session.get('2fa'):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({'message': f'Hello, {session["username"]}! You have successfully logged in with 2FA.'}), 200

if __name__ == '__main__':
    app.run(debug=True)