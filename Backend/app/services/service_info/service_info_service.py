import jwt
import datetime
from flask import jsonify
from functools import wraps
from flask import request, jsonify, current_app
from app.repository.services.service_info_repository import ServiceInfoRepository
from app.repository.customer.customer_repository import CustomerRepository
from app.repository.service_professional.service_professional_info import ServiceProfessionalRepository

class ServiceInfoService:
    @staticmethod
    def service_info_fetch_by_user_location(user_id, role):
        if role == "customer":
            user_data = CustomerRepository.fetch_by_user_id(user_id)
        elif role == "service_professional":
            user_data = ServiceProfessionalRepository.fetch_by_user_id(user_id)
        else:
            return jsonify({"message": "Invalid role"}), 400
        
        if not user_data:
            return jsonify({"message": "User not found"}), 404

        city, state, country = user_data[0].city, user_data[0].state, user_data[0].country
        services = ServiceInfoRepository.fetch_by_location_state_country(city, state, country)
        services_data = [
            {
                "service_id": service.service_id,
                "description": service.description,
                "currency": service.currency,
                "base_price": service.base_price,
                "city": service.city,
                "state": service.state,
                "country": service.country,
            }
            for service in services
        ]
        return jsonify(services_data), 200