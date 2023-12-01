import secrets
from datetime import datetime, timedelta
from re import match

import psycopg2
from flask import Flask, render_template, request, url_for, redirect, flash, abort, jsonify
import bcrypt
import jwt
from flask_cors import CORS

from Captcha.first_main import *

app = Flask(__name__)
cors = CORS(app)


def get_db_connection():
    try:
        conn = psycopg2.connectcon = psycopg2.connect(
            database="SportSpot",
            user="postgres",
            password="htl123",
            host="localhost",
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
        # 'username': username,
        # 'firstname': firstname,
        # 'surname': surname,
        # 'birthdate' : birthdate,
        # 'email' : email,
        # 'fav_sports' : fav_sports,
        # 'gender' : gender,
        # 'postal_code' : postal_code,
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return abort(404)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return abort(404)

    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
            cur.close()
            conn.close()
            user_id = user[0]
            token = generate_token(user_id)
            # token = generate_token(user_id, user[1], user[2], user[3], user[5], user[6], user[7], user[8], user[9])
            user_data = {"id": user[0], "firstname": user[1], "surname": user[2], "username": user[3],
                         "birthdate": user[5], "email": user[6], "fav_sports": user[7], "gender": user[8],
                         "postal_code": user[9]}
            # kein Passwort
            return jsonify({'token': token, 'user': user_data})

        else:
            return abort(404)


# Konvertiert das Geschlecht da Auswahl zwischen (male, female, other), aber Speicherung in der Datenbank
# als (m, f, o)
def convert_gender(gender):
    return gender[0].lower() if gender in ['male', 'female'] else 'o'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return abort(404)
    firstname = data.get('firstname')
    surname = data.get('surname')
    username = data.get('username')
    password = data.get('password')
    birthdate = data.get('birthdate')
    email = data.get('email')
    fav_sports = data.get('sports')
    gender = convert_gender(data.get('gender'))
    postal_code = data.get('postalcode')

    if not username or not password:
        return abort(404)
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            conn.close()
            return jsonify({'message': 'Username already exists'}), 400  # Return an error
        else:
            # Verifizierung
            if not firstname or len(firstname.strip()) < 2:
                return jsonify({'message': 'Vorname muss mindestens 2 Zeichen lang sein'}), 400

            if not surname or len(surname.strip()) < 2:
                return jsonify({'message': 'Nachname muss mindestens 2 Zeichen lang sein'}), 400

            if not username or len(username.strip()) < 2:
                return jsonify({'message': 'Username muss mindestens 2 Zeichen lang sein'}), 400

            if match(r"^(?=.*\d)(?=.*[A-Z]).{9}$", password):
                return jsonify(
                    {'message': 'Das Passwort muss eine Ziffer, einen Großbuchstaben und neun Zeichen lang sein'}), 400

            if not email or '@' not in email:
                return jsonify({'message': 'Vorname muss mindestens 2 Zeichen lang sein'}), 400

            if not postal_code:
                return jsonify({'message': 'Wir benötigen als Sicherheitsmaßnahme ihre Postleizahl'}), 400

            if not fav_sports:  # nicht mehr benötigt?
                fav_sports = []

            if not gender:
                gender = 'o'

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            cur.execute(
                'INSERT INTO users (firstname, surname, username, password, birthdate, email, fav_sports, '
                'gender, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (firstname, surname, username, hashed_password.decode('utf-8'), birthdate, email, fav_sports, gender,
                 postal_code))
            conn.commit()

            cur.close()
            conn.close()
            return jsonify({'message': 'Registration successful'}), 201
    else:
        return abort(404)


@app.route('/allUsers', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        cur.close()
        conn.close()
        users_json = [{"id": row[0], "username": row[1]} for row in users]
        return jsonify(users_json)
    else:
        return abort(404)


@app.route('/saveSportsToUser', methods=['POST'])
def save_sports_to_user():
    data = request.get_json()
    if not data:
        return abort(404)
    email = data.get('email')
    sports = data.get('selectedSports')

    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('UPDATE users SET fav_sports = %s WHERE email = %s;', (sports, email))
        conn.commit()
        return jsonify({'message': f'Sports to user with the email {email} successfully changed'}), 201
    return jsonify({'message': 'sports could not be added'}), 404


@app.route('/delete/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE id = %s;', (user_id,))
        conn.commit()
        return jsonify({'message': f'User {user_id} successfully deleted'}), 201

    return jsonify({'message': 'not deleted'}), 404


##########
# Captcha
##########
@app.route("/getCaptcha", methods=["GET"])
def get_captcha_data():
    svg_path = 'Captcha/captcha.svg'

    text_captcha = generate_captcha_text(5)
    create_captcha_svg(text_captcha)

    with open(svg_path, 'r') as svg_file:
        svg_content = svg_file.read()

    conn = get_db_connection()

    # Saving the SVG content and creating an ID
    if conn is not None:
        cur = conn.cursor()
        cur.execute('INSERT INTO captcha (text) VALUES (%s) RETURNING id', (text_captcha,))
        last_captcha_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    else:
        print("Not possible to save captcha")

    response_data = {
        'captcha_id': last_captcha_id,
        'svg': svg_content
    }

    return jsonify(response_data)

@app.route("/compareInput", methods=["GET"])
def get_last_captcha_id():
    pass



if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
