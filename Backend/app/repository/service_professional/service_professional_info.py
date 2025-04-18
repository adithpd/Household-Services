from app.models.service_professional.service_professional_info import ServiceProfessionalInfo
from app.models.db import db

class ServiceProfessionalRepository:
    @staticmethod
    def insert_service_professional_record(service_professional_data):
        service_professional_record = ServiceProfessionalInfo(
            user_id=service_professional_data["user_id"],
            name=service_professional_data["name"],
            phone=service_professional_data["phone"],
            description=service_professional_data["description"],
            experience_years=service_professional_data["experience_years"],
            service_keywords=None,
            service_id=service_professional_data.get("service_id"),
            location=service_professional_data["location"], 
            city=service_professional_data["city"],
            state=service_professional_data["state"],
            country=service_professional_data["country"],
            pincode=service_professional_data["pincode"],
        )
        db.session.add(service_professional_record)
        db.session.commit()
        return service_professional_record
    
    @staticmethod    
    def fetch_by_user_id(user_id):
        service_professional_record = ServiceProfessionalInfo.query.filter((ServiceProfessionalInfo.user_id==user_id)).all()
        return service_professional_record
    
    @staticmethod    
    def fetch_by_service_professional_id(service_professional_id):
        service_professional_record = ServiceProfessionalInfo.query.filter((ServiceProfessionalInfo.service_professional_id==service_professional_id)).all()
        return service_professional_record
    
    @staticmethod
    def fetch_by_service_location(query):
        service_professional_records = ServiceProfessionalInfo.query.filter(
            (ServiceProfessionalInfo.description.ilike(f"%{query}%")) |
            (ServiceProfessionalInfo.location.ilike(f"%{query}%")) |
            (ServiceProfessionalInfo.city.ilike(f"%{query}%")) |
            (ServiceProfessionalInfo.state.ilike(f"%{query}%")) |
            (ServiceProfessionalInfo.country.ilike(f"%{query}%")) |
            (ServiceProfessionalInfo.pincode.ilike(f"%{query}%"))
        ).all()
        return service_professional_records