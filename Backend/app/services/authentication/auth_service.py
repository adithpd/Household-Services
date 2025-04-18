import jwt
import datetime
from flask import jsonify
from functools import wraps
from flask import request, jsonify, current_app
from app.repository.user.user_repository import UserRepository
from app.repository.token.token_repository import TokenRepository

class AuthService:
    @staticmethod
    def register(registry_data):
        if not registry_data or not registry_data.get('user_id') or not registry_data.get('name') or not registry_data.get('email') or not registry_data.get('password') or not registry_data.get('role'):
            return jsonify({'message': 'Request does not contain data for required fields'}), 422

        if UserRepository.fetch_by_user_id(registry_data['user_id']) or UserRepository.fetch_by_email_id( registry_data['email']):
            return jsonify({'message': 'Request conflicts as username or email already exists'}), 409
            
        UserRepository.insert_user_record(registry_data)
        return jsonify({"message": "Registration is successful"}), 200
    
    @staticmethod
    def login(auth_data, secret_key):
        if not auth_data or not auth_data.get('user_id') or not auth_data.get('password'):
            return jsonify({'message': 'Could not verify'}), 401

        
        
        user_record = UserRepository.fetch_by_user_id(auth_data['user_id'])
        if(user_record):
            if user_record.password == auth_data['password']:
                token = AuthService.generate_token(auth_data['user_id'], secret_key)
                return jsonify({
                    'message': "Login Successful",
                    'token': token,
                    'user_id': auth_data['user_id'],
                    'role': user_record.role,
                }), 200

            return jsonify({'message': 'Invalid credentials'}), 401
        return jsonify({'message': 'Username/Password is invalid'}), 401

    @staticmethod
    def logout():
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Blacklist the token
            TokenRepository.blacklist_token(token)
            return jsonify({'message': 'Successfully logged out.'}), 200
        except Exception:
            return jsonify({'message': 'An error occurred during logout.'}), 500
    


    @staticmethod
    def verify_token():
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                print("Request Headers:", request.headers)
                token = request.headers.get('X-Access-Token')

                if not token:
                    print(token)
                    return jsonify({'message': 'Token is missing!'}), 403

                if TokenRepository.is_token_blacklisted(token):
                    return jsonify({'message': 'Token is invalidated!'}), 403

                try:
                    secret_key = current_app.config['SECRET_KEY']
                    data = AuthService.decode_token(token, secret_key)
                    current_user = data['user']
                except Exception:
                    return jsonify({'message': 'Token is invalid!'}), 403

                return f(current_user, *args, **kwargs)
            return decorated
        return decorator

    @staticmethod
    def generate_token(username, secret_key):
        return jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, secret_key, algorithm="HS256")

    @staticmethod
    def decode_token(token, secret_key):
        return jwt.decode(token, secret_key, algorithms=["HS256"])
