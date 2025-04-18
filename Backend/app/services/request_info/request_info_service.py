import jwt
import datetime
from flask import jsonify
from functools import wraps
from flask import request, jsonify, current_app
from app.repository.request_info.request_info_repository import RequestInfoRepository
from app.repository.customer.customer_repository import CustomerRepository
from datetime import datetime
from app import cache, redis_client


class RequestInfoService:
    @staticmethod
    def request_info_insert(request_data):
        try:
            if request_data["role"] != "customer":
                    return jsonify({"message": "Invalid role"}), 400
            
            customer_data = CustomerRepository.fetch_by_user_id(request_data["user_id"])
            if not customer_data:
                return jsonify({"message": "Customer not found"}), 404

            customer_id = customer_data[0].customer_id
            start_time = datetime.strptime(request_data["start_time"], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(request_data["end_time"], "%Y-%m-%d %H:%M:%S")
            
            RequestInfoRepository.insert_request(
                customer_id=customer_id,
                keywords=request_data["service_description"],
                service_id=request_data["service_id"],
                start_time=start_time,
                end_time=end_time,
                currency=request_data["currency"],
                quote_price=request_data["quote_price"],
                status=request_data["status"]
            )
            cache.delete('request_info')
            return jsonify({"message": "Request created successfully"}), 201

        except Exception as e:
            print(e)
            return jsonify({"message": "Error inserting request", "error": str(e)}), 500
        
    @staticmethod
    @cache.cached(timeout=60, key_prefix='request_info')
    def request_info_view_by_customer_id(request_data):
        cached_response = redis_client.get('request_info')
        if cached_response:
          return jsonify(cached_response)
        try:
            if request_data["role"] != "customer":
                    return jsonify({"message": "Invalid role"}), 400
            
            customer_data = CustomerRepository.fetch_by_user_id(request_data["user_id"])
            if not customer_data:
                return jsonify({"message": "Customer not found"}), 404

            customer_id = customer_data[0].customer_id
            requests = RequestInfoRepository.fetch_new_requests_by_customer(customer_id)
            return jsonify({"requests": [req.to_dict() for req in requests]}), 200

        except Exception as e:
            print(e)
            return jsonify({"message": "Error inserting request", "error": str(e)}), 500
    
    @staticmethod
    def request_info_cancel_by_customer_id(request_data):
        try:
            if request_data.get("role") != "customer":
                return jsonify({"message": "Invalid role"}), 400

            customer_data = CustomerRepository.fetch_by_user_id(request_data.get("user_id"))
            if not customer_data:
                return jsonify({"message": "Customer not found"}), 404

            customer_id = customer_data[0].customer_id
            request_id = request_data.get("request_id")

            request_record = RequestInfoRepository.fetch_request_by_id_and_customer(customer_id, request_id)

            if not request_record:
                return jsonify({"message": "Request not found or already processed"}), 404

            if request_record.status != "NEW":
                return jsonify({"message": "Only NEW requests can be canceled"}), 400

            RequestInfoRepository.delete_request_by_id(request_id)
            cache.delete('request_info')
            return jsonify({"message": "Request canceled successfully"}), 200

        except Exception as e:
            print(f"Error in cancel_request: {e}")
            return jsonify({"message": "Error canceling request", "error": str(e)}), 500