from flask import request, jsonify
from app.services.service_info.service_info_service import ServiceInfoService
from flask import jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["500 per day", "100 per hour"]
)

def service_info_routes(app):
    limiter.init_app(app)
    
    
    @app.route('/service-info/fetch/by/user/location', methods=['GET'])
    @limiter.limit("30 per minute")
    def service_info_fetch_by_user_location():
        user_id = request.args.get("user_id")
        role = request.args.get("role")
        return ServiceInfoService.service_info_fetch_by_user_location(user_id, role)
    
