from flask import request, jsonify
from app.services.authentication.auth_service import AuthService
from flask import jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["200 per day", "50 per hour"]
)

def authentication_routes(app):
    limiter.init_app(app)
    
    @limiter.limit("5 per minute")
    @app.route('/register', methods=['POST'])
    def register():
        registry_data = request.json
        return AuthService.register(registry_data)
    
    @limiter.limit("10 per minute")
    @app.route('/login', methods=['POST'])
    def login():
        auth_data = request.json
        return AuthService.login(auth_data, app.config['SECRET_KEY'])
    
    @app.route('/logout', methods=['POST'])
    @AuthService.verify_token()
    @limiter.limit("30 per minute")
    def logout(current_user):
        return AuthService.logout()
    
    @app.route('/protected', methods=['GET'])
    @AuthService.verify_token()
    @limiter.limit("100 per hour")
    def protected_route(current_user):
        return jsonify({'message': f'Welcome {current_user}! This is a protected route.'})

    @app.route('/', methods=['GET'])
    @limiter.limit("100 per hour")
    def hello():
        return "Hello!\n\nStored in authentication controller\n\nYou are now in root of domain"