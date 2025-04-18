from app.models.services.service_info import ServiceInfo
from app.models.db import db
from sqlalchemy import and_


class ServiceInfoRepository:
    @staticmethod
    def insert_service_record(service_data):
        service_record = ServiceInfo(description=service_data['description'], currency=service_data['currency'], base_price=service_data['base_price'], city=service_data['city'], state=service_data['state'], country=service_data['country'])
        db.session.add(service_record)
        db.session.commit()
        return service_record
    
    @staticmethod
    def fetch_all_service_id():
        service_records = db.session.query(ServiceInfo).all()
        result = [
            {
                "service_id": service.service_id,
                "description": service.description,
                "currency": service.currency,
                "base_price": service.base_price,
                "created_at": service.created_at,
                "city": service.city,
                "state": service.state,
                "country": service.country,
            }
            for service in service_records
        ]
        
        return result

    
    @staticmethod
    def fetch_by_service_id(service_id):
        service_record = ServiceInfo.query.filter((ServiceInfo.service_id == service_id)).first()
        return service_record
    
    @staticmethod
    def fetch_by_description(description):
        service_record = ServiceInfo.query.filter((ServiceInfo.description == description)).all()
        return service_record
    
    @staticmethod
    def fetch_by_currency(currency):
        service_record = ServiceInfo.query.filter((ServiceInfo.currency == currency)).all()
        return service_record
    
    @staticmethod
    def fetch_by_base_price(base_price):
        service_record = ServiceInfo.query.filter((ServiceInfo.base_price == base_price)).all()
        return service_record
    
    @staticmethod
    def fetch_by_location_state_country(city, state, country):
        service_records = ServiceInfo.query.filter(and_(ServiceInfo.city == city, ServiceInfo.state == state, ServiceInfo.country == country)).all()
        return service_records
    
    @staticmethod
    def update_service_description(service_id, new_description):
        service_record = ServiceInfo.query.filter_by(service_id=service_id).first()
        if service_record:
            service_record.description = new_description
            db.session.commit()
            return service_record
        return None

    @staticmethod
    def update_service_currency(service_id, new_currency):
        service_record = ServiceInfo.query.filter_by(service_id=service_id).first()
        if service_record:
            service_record.currency = new_currency
            db.session.commit()
            return service_record
        return None

    @staticmethod
    def update_service_base_price(service_id, new_base_price):
        service_record = ServiceInfo.query.filter_by(service_id=service_id).first()
        if service_record:
            service_record.base_price = new_base_price
            db.session.commit()
            return service_record
        return None

    @staticmethod
    def delete_by_service_id(service_id):
        service_record = ServiceInfo.query.filter_by(service_id=service_id).first()
        db.session.delete(service_record)
        db.session.commit()
        return None
    
    @staticmethod
    def service_info_edit(service_id, description, currency, base_price):
        service = ServiceInfo.query.filter_by(service_id=service_id).first()
        if description:
            service.description = description
        if currency:
            service.currency = currency
        if base_price:
            service.base_price = base_price
        db.session.commit()
        return None