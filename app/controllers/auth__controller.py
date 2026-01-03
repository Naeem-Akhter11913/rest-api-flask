from pymongo.errors import PyMongoError
from flask import jsonify, request
from datetime import datetime , timedelta

from flask_jwt_extended import create_access_token , set_access_cookies, get_csrf_token
from ..extention import mongo
from ..extention import bcrypt
import json



ACCESS_EXPIRES = timedelta(hours=1)


def create__user__registration():
    try:
        user__details = request.get_json()
        

        user__already__present = mongo.db.auth__schema.find_one({'email': user__details.get('email')})

        if user__already__present:
            return jsonify({
                'status': False,
                'message': 'This Email is already exist'
            }), 409
        
        if '@' not in user__details.get('email'):
            return jsonify({
                'status': False,
                'message': 'Invalid Email!'
            }), 400
        
        if len(user__details.get('name')) <= 3:
            return jsonify({
                'status': False,
                'message': 'Name should be atleast 3 latter!'
            }), 400
        
        if user__details.get('password') != user__details.get('confirm__password'):
            return jsonify({
                'status': False,
                'message':'Sorry! Password is missmatched!'
            })

        hash__pashword = bcrypt.generate_password_hash(user__details.get('password')).decode('utf-8')
        now = datetime.utcnow()
        users = {
            'name': user__details.get('name'),
            'email': user__details.get('email'),
            'password': hash__pashword,
            'createdAt': now,
            'updatedAt': now
        }
        mongo.db.auth__schema.insert_one(users)
        return jsonify({
            'status': True,
            'message': 'User Registration Success!'
        })
    except PyMongoError as e:
        return jsonify({
            'status': False,
            'message':f"Database error: {str(e)}",
        }), 500
    except Exception as e:
        return jsonify({
            'status': False,
            'message': f'Internal Server Error: {str(e)}'
        }), 500
    

def create__user__login():
    try:
        user_login_details = request.get_json()
        email = user_login_details.get('email')
        password = user_login_details.get('password')

        user = mongo.db.auth__schema.find_one({'email': email})
        if not user:
            return jsonify({
                'status': False,
                'message': 'User does not exist!'
            }), 401

        if not bcrypt.check_password_hash(user.get('password'), password):
            return jsonify({
                'status': False,
                'message': 'Password mismatched!'
            }), 400

        token_data = {
            '_id': str(user['_id']),
            'name': user['name'],
            'email': user['email']
        }

        # access_token = create_access_token(identity=token_data)
        access_token = create_access_token(
        identity=token_data["_id"],                  # 👈 sub must be string
        additional_claims={"user": token_data}      # 👈 put full user data here
)

        # 👉 extract csrf token from the access token
        csrf_token = get_csrf_token(access_token)

        response = jsonify({
            'status': True,
            'message': 'Logged in successfully!',
            'csrf_token': csrf_token   # 👈 return it for Postman
        })

        set_access_cookies(response, access_token)
        return response, 200

    except PyMongoError as e:
        return jsonify({'status': False, 'message': f'Database Error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'status': False, 'message': f'Internal Server Error: {str(e)}'}), 500
