from functools import wraps
from flask import request, jsonify
from ..extention import jwt
import os

def auth__required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'status': False,
                'message': 'Unauthorized access'
            }), 401
        token = token.split(' ')[1]

        # if token != os.getenv('SECURITY_KEY'):
        #     return jsonify({
        #         'status': False,
        #         'message': 'Unauthorized access'
        #     }), 401
     
        return fn(*args, **kwargs)
    return wrapper