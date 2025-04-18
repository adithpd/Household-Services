from flask import request, jsonify
from app.services.request_info.request_info_service import RequestInfoService
from flask import jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["500 per day", "100 per hour"]
)

def request_info_routes(app):
    @app.route('/request-info/insert', methods=['POST'])
    @limiter.limit("10 per minute")
    def request_info_insert():
        request_data = request.json
        return RequestInfoService.request_info_insert(request_data)
    
    @app.route('/request-info/view/customer/all', methods=['POST'])
    @limiter.limit("30 per minute")
    def request_info_view_by_customer_id():
        request_data = request.json
        return RequestInfoService.request_info_view_by_customer_id(request_data)
    
    @app.route('/request-info/cancel/customer', methods=['DELETE'])
    @limiter.limit("5 per minute")
    def request_info_cancel_by_customer_id():
        request_data = request.json
        return RequestInfoService.request_info_cancel_by_customer_id(request_data)
    
