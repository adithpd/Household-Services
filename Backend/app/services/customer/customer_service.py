import jwt
import datetime
from flask import jsonify
from functools import wraps
from flask import request, jsonify, current_app
from app.repository.customer.customer_repository import CustomerRepository
from app.repository.booking_info.booking_info_repository import BookingInfoRepository
from app.repository.request_info.request_info_repository import RequestInfoRepository
from app.repository.user.user_repository import UserRepository
from app.repository.service_professional.service_professional_info import ServiceProfessionalRepository
from app.repository.review_info.review_info_repository import ReviewInfoRepository
from app.repository.services.service_info_repository import ServiceInfoRepository
from app import cache, redis_client

class CustomerService:
    @staticmethod
    def register(customer_data):
        if not customer_data or not customer_data.get('user_id') or not customer_data.get('location') or not customer_data.get('city') or not customer_data.get('state') or not customer_data.get('country') or not customer_data.get('pincode') or not customer_data.get('phone'):
            return jsonify({'message': 'Request does not contain data for required fields'}), 422

        if CustomerRepository.fetch_by_user_id(customer_data['user_id']):
            return jsonify({'message': 'Request conflicts as customer exists with that username'}), 409
            
        CustomerRepository.insert_customer_record(customer_data)
        cache.delete('customer_info')
        return jsonify({"message": "Customer record succesfully inserted!"}), 200
    
    @staticmethod
    def update_blocked_status(customer_id, blocked):
        update_blocked_status = CustomerRepository.update_blocked_by_customer_id(customer_id, blocked)
        if not update_blocked_status:
            return jsonify({"error": "No customer found for updating blocked status"}), 404
        
        cache.delete('customer_info')
        return jsonify({"message": "blocked status updated for the customer"}), 200
    
    @staticmethod
    @cache.cached(timeout=60, key_prefix='booking_info')
    def view_booking_info_customer_completed(customer_data):
        cached_response = redis_client.get('booking_info')
        if cached_response:
          return jsonify(cached_response)
      
        user_id = customer_data["user_id"]
        customer = CustomerRepository.fetch_by_user_id(user_id)
        if not customer:
            return jsonify({"message": "Customer not found"}), 404
        customer_id = customer[0].customer_id
        all_bookings = BookingInfoRepository.fetch_booking_info_by_customer_id_completed(customer_id)
        response_data = []
        for booking in all_bookings:
            request_record = RequestInfoRepository.fetch_accepted_requests_by_request_id(booking.booking_id)
            service_professional_record = ServiceProfessionalRepository.fetch_by_service_professional_id(booking.service_professional_id)
            user_record = UserRepository.fetch_by_user_id(service_professional_record[0].user_id)
            response_data.append({
                "booking_id": booking.booking_id,
                "service_professional_id": booking.service_professional_id,
                "customer_id": booking.customer_id,
                "start_time": booking.start_time.isoformat(),
                "end_time": booking.end_time.isoformat(),
                "currency": booking.currency,
                "price": booking.price,
                "status": booking.status,
                "service_professional_name": user_record.name,
                "keywords": request_record.keywords,
            })
        return jsonify({"bookings": response_data}), 200
    
    @staticmethod
    def mark_review_info_customer_completed(review_data):
        required_fields = ["booking_id", "service_professional_rating", "review_provided", "customer_remarks", "paid_price", "user_id"]
        if not all(field in review_data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 422

        customer = CustomerRepository.fetch_by_user_id(review_data["user_id"])
        if not customer:
            return jsonify({"message": "Customer not found"}), 404

        existing_review = ReviewInfoRepository.fetch_by_booking_id(review_data["booking_id"])
        if not existing_review:
            return jsonify({"message": "Review record missing for mentioned booking"}), 409

        review_id = existing_review.review_id
        ReviewInfoRepository.update_review_info_by_review_id(review_id, review_data)
        cache.delete('review_info')
        return jsonify({"message": "Review submitted successfully"}), 201
    
    @staticmethod
    @cache.cached(timeout=60, key_prefix='booking_info')
    def view_booking_info_customer(customer_data):
        cached_response = redis_client.get('booking_info')
        if cached_response:
          return jsonify(cached_response)
      
        user_id = customer_data["user_id"]
        customer = CustomerRepository.fetch_by_user_id(user_id)
        if not customer:
            return jsonify({"message": "Customer not found"}), 404
        customer_id = customer[0].customer_id
        all_bookings = BookingInfoRepository.fetch_booking_info_by_customer_id(customer_id)
        response_data = []
        for booking in all_bookings:
            request_record = RequestInfoRepository.fetch_accepted_requests_by_request_id(booking.booking_id)
            service_professional_record = ServiceProfessionalRepository.fetch_by_service_professional_id(booking.service_professional_id)
            user_record = UserRepository.fetch_by_user_id(service_professional_record[0].user_id)
            response_data.append({
                "booking_id": booking.booking_id,
                "service_professional_id": booking.service_professional_id,
                "customer_id": booking.customer_id,
                "start_time": booking.start_time.isoformat(),
                "end_time": booking.end_time.isoformat(),
                "currency": booking.currency,
                "price": booking.price,
                "status": booking.status,
                "service_professional_name": user_record.name,
                "keywords": request_record.keywords,
            })
        return jsonify({"bookings": response_data}), 200
    
    def fetch_services(query):
        if not query:
            return jsonify([])
        
        results = ServiceProfessionalRepository.fetch_by_service_location(query)
        data = []

        if not results:
            return jsonify(data), 200
        
        for result in results:
            if not result:
                return jsonify(data), 200
            
            service_id = result.service_id
            if not service_id:
                return jsonify(data), 200
            
            service_info = ServiceInfoRepository.fetch_by_service_id(service_id=service_id)
            data.append({"service_name": service_info.description, "location": result.location, "city": result.city, "state": result.state, "country": result.country, "pincode": result.pincode, "service_id": service_info.service_id, "currency": service_info.currency, "base_price": float(service_info.base_price)})
            print(data)
            
        return jsonify(data), 200
    
    def fetch_blocked_by_user_id(user_id):
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        customer = CustomerRepository.fetch_by_user_id(user_id)[0]
        
        if not customer:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"blocked": customer.blocked}), 200