from app.models.booking.booking_info import BookingInfo
from app.models.db import db
from sqlalchemy import and_

class BookingInfoRepository:
    @staticmethod
    def insert_booking_record(booking_data):
        booking_record = BookingInfo(
            booking_id=booking_data["booking_id"],
            customer_id=booking_data["customer_id"], 
            service_professional_id=booking_data["service_professional_id"],
            start_time=booking_data["start_time"],
            end_time=booking_data["end_time"],
            status=booking_data["status"],
            currency=booking_data["currency"],
            price=booking_data["price"]
        )
        db.session.add(booking_record)
        db.session.commit()
        return booking_record
    
    @staticmethod
    def fetch_booking_info_by_service_professional_id(service_professional_id):
        booking_records = BookingInfo.query.filter((BookingInfo.service_professional_id==service_professional_id)).all()
        return booking_records
    
    @staticmethod
    def fetch_booking_info_by_customer_id(customer_id):
        booking_records = BookingInfo.query.filter((BookingInfo.customer_id==customer_id)).all()
        return booking_records
    
    @staticmethod
    def fetch_booking_info_by_customer_id_completed(customer_id):
        booking_records = BookingInfo.query.filter(and_(BookingInfo.customer_id==customer_id, BookingInfo.status == 'COMPLETED')).all()
        return booking_records
    
    @staticmethod
    def fetch_booking_info_by_service_professional_id_completed(service_professional_id):
        booking_records = BookingInfo.query.filter(and_(BookingInfo.service_professional_id==service_professional_id, BookingInfo.status == 'COMPLETED')).all()
        return booking_records
    
    @staticmethod
    def fetch_booking_info_by_booking_id(booking_id):
        booking_records = BookingInfo.query.filter((BookingInfo.booking_id==booking_id)).all()
        return booking_records
    
    @staticmethod
    def delete_by_booking_id(booking_id):
        booking_record = BookingInfo.query.filter_by(booking_id=booking_id).first()
        if booking_record:
            db.session.delete(booking_record)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def mark_complete_by_booking_id(booking_id, service_professional_remarks, customer_rating):
        booking_record = BookingInfo.query.filter_by(booking_id=booking_id).first()
        if booking_record:
            booking_record.status = "COMPLETED"
            booking_record.service_professional_remarks = service_professional_remarks 
            booking_record.customer_rating = customer_rating
            db.session.commit()
        return None