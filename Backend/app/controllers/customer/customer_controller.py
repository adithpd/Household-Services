from flask import request, jsonify, make_response
from app.services.customer.customer_service import CustomerService
from flask import jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
)


def customer_routes(app):
    limiter.init_app(app)
        
    @app.route('/customer/register', methods=['POST'])
    @limiter.limit("5 per minute")
    def customer_insert():
        customer_data = request.json
        return CustomerService.register(customer_data)
    
    @app.route('/customer/blocked', methods=['GET'])
    @limiter.limit("20 per minute")
    def update_blocked_status():
        customer_id = request.args.get("customer_id")
        blocked = request.args.get("blocked")
        return CustomerService.update_blocked_status(customer_id, blocked)
    
    @app.route('/customer/booking-info/view', methods=['POST'])
    @limiter.limit("20 per minute")
    def view_booking_info_customer():
        customer_data = request.json
        return CustomerService.view_booking_info_customer(customer_data)
    
    @app.route('/customer/booking-info/view/completed', methods=['POST'])
    @limiter.limit("20 per minute")
    def view_booking_info_customer_completed():
        customer_data = request.json
        return CustomerService.view_booking_info_customer_completed(customer_data)
    
    @app.route('/customer/review-info/completed', methods=['POST'])
    @limiter.limit("10 per minute")
    def mark_review_info_customer_completed():
        review_data = request.json
        return CustomerService.mark_review_info_customer_completed(review_data)
    

    @app.route("/search-services", methods=["GET"])
    def search_services():
        query = request.args.get("q", "")
        if not query:
            return jsonify([])
        
        return CustomerService.fetch_services(query)
    
    @app.route("/customer/verify-status", methods=["GET"])
    def verify_status_customer():
        user_id = request.args.get("user_id")
        return CustomerService.fetch_blocked_by_user_id(user_id)
        
        
        