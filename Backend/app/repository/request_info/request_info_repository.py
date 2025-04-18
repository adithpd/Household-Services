from app.models.request.request_info import RequestInfo
from app.models.db import db

class RequestInfoRepository:
    @staticmethod
    def insert_request(customer_id, keywords, service_id, start_time, end_time, currency, quote_price, status):
        request_record = RequestInfo(
            customer_id=customer_id,
            keywords=keywords,
            service_id=service_id,
            start_time=start_time,
            end_time=end_time,
            currency=currency,
            quote_price=quote_price,
            status=status
        )
        db.session.add(request_record)
        db.session.commit()
        return request_record
    
    @staticmethod
    def fetch_new_requests_by_customer(customer_id):
        return (
            RequestInfo.query
            .filter_by(customer_id=customer_id, status="NEW")
            .order_by(RequestInfo.start_time.desc())
            .all()
        )
    
    @staticmethod
    def fetch_live_requests_by_service_id(service_id):
        return (
            RequestInfo.query
            .filter_by(service_id=service_id, status="NEW")
            .order_by(RequestInfo.start_time.desc())
            .all()
        )
    
    @staticmethod
    def fetch_requests_by_request_id(request_id):
        return (
            RequestInfo.query
            .filter_by(request_id=request_id)
            .all()
        )
    
    @staticmethod
    def fetch_request_by_id_and_customer(customer_id, request_id):
        return (
            RequestInfo.query
            .filter_by(customer_id=customer_id, request_id=request_id, status="NEW")
            .first()
        )
    @staticmethod
    def delete_request_by_id(request_id):
        request_record = RequestInfo.query.filter_by(request_id=request_id, status="NEW").first()
        if request_record:
            request_record.status = "CANCELED"
            db.session.commit()
        return request_record
    
    @staticmethod
    def update_request_status(request_id, request_status):
        request_record = RequestInfo.query.filter_by(request_id=request_id).first()
        if request_record:
            request_record.status = request_status
            db.session.commit()
            
        return None
    
    @staticmethod
    def fetch_accepted_requests_by_request_id(request_id):
        return (
            RequestInfo.query
            .filter_by(request_id=request_id, status="ACCEPTED")
            .first()
        )
    
    @staticmethod
    def delete_by_request_id(request_id):
        request_record = RequestInfo.query.filter_by(request_id=request_id).first()
        if request_record:
            db.session.delete(request_record)
            db.session.commit()
            return True
        return False