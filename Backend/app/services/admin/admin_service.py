from flask import jsonify
from app.repository.services.service_info_repository import ServiceInfoRepository
from app.models.service_professional.service_professional_info import ServiceProfessionalInfo
from app.models.service_professional.service_professional_documents import ServiceProfessionalDocuments
from app.models.reviews.reviews_info import ReviewsInfo
from app.models.user.user_info import UserInfo
from app.models.customer.customer_info import CustomerInfo
from app.models.booking.booking_info import BookingInfo
from app.models.db import db
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased

class AdminService:
    @staticmethod
    def create_service(service_data):
        if not service_data or not service_data['description'] or not service_data['currency'] or not service_data['base_price'] or not service_data['city'] or not service_data['state'] or not service_data['country']:
            return jsonify({'message': 'Request does not contain data for required fields'}), 422
            
        ServiceInfoRepository.insert_service_record(service_data)
        return jsonify({"message": "Service is successfully created"}), 200
    
    @staticmethod
    def service_professional_verification_data():
        query = (
            db.session.query(
                ServiceProfessionalInfo.service_professional_id,
                ServiceProfessionalInfo.name,
                ServiceProfessionalInfo.phone,
                UserInfo.email,
                ServiceProfessionalInfo.description,
                ServiceProfessionalDocuments.verified,
                func.coalesce(func.avg(ReviewsInfo.service_professional_rating), 0).label("average_rating"),
            )
            .join(ServiceProfessionalInfo, ServiceProfessionalInfo.service_professional_id == ServiceProfessionalDocuments.service_professional_id)
            .join(UserInfo, UserInfo.user_id == ServiceProfessionalInfo.user_id)
            .outerjoin(ReviewsInfo, ServiceProfessionalInfo.service_professional_id == ReviewsInfo.service_professional_id)
            .group_by(
                ServiceProfessionalInfo.service_professional_id,
                ServiceProfessionalDocuments.verified
            )
            .all()
        )
        result = [
            {
                "service_professional_id": row.service_professional_id,
                "name": row.name,
                "verified": row.verified,
                "email": row.email,
                "phone": row.phone,
                "description": row.description,
                "rating": int(row.average_rating),
            }
            for row in query
        ]
        return jsonify(result), 200
    
    @staticmethod
    def customer_data():
        query = (
            db.session.query(
                CustomerInfo.customer_id,
                UserInfo.user_id,
                CustomerInfo.blocked,
                CustomerInfo.city,
                CustomerInfo.state,
                CustomerInfo.country,
                CustomerInfo.created_at,
                func.coalesce(func.avg(BookingInfo.customer_rating), 0).label("average_rating"),
            )
            .join(UserInfo, UserInfo.user_id == CustomerInfo.user_id)
            .outerjoin(BookingInfo, CustomerInfo.customer_id == BookingInfo.customer_id)
            .group_by(
                CustomerInfo.customer_id,
                CustomerInfo.blocked
            )
            .all()
        )
        result = [
            {
                "customer_id": row.customer_id,
                "user_id": row.user_id,
                "blocked": row.blocked,
                "city": row.city,
                "state": row.state,
                "country": row.country,
                "created_at": row.created_at,
                "average_rating": int(row.average_rating),
            }
            for row in query
        ]
        return jsonify(result), 200
    
    @staticmethod
    def service_info_data():
        result = ServiceInfoRepository.fetch_all_service_id()
        return jsonify(result), 200
    
    @staticmethod
    def service_info_delete(service_data):
        service_id = service_data.get("service_id")
        if not service_id:
            return jsonify({"message": "Service ID is required"}), 400

        ServiceInfoRepository.delete_by_service_id(service_id)
        return jsonify({"message": f"Service {service_id} deleted successfully"}), 200
    
    @staticmethod
    def service_info_edit(service_data):
        service_id = service_data.get('service_id')
        description = service_data.get('description')
        currency = service_data.get('currency')
        base_price = service_data.get('base_price')
        service = ServiceInfoRepository.fetch_by_service_id(service_id=service_id)
        if not service:
            return jsonify({'message': 'Service not found'}), 404
        
        service = ServiceInfoRepository.service_info_edit(service_id=service_id, description=description, currency=currency, base_price=base_price)
        return jsonify({'message': 'Service updated successfully'}), 200