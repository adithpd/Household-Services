from ..db import db
import uuid
from ..customer.customer_info import CustomerInfo
from ..service_professional.service_professional_info import ServiceProfessionalInfo

def generate_uuid():
    return uuid.uuid4().hex

class BookingInfo(db.Model):
    __tablename__ = "booking_info"
    booking_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    service_professional_id = db.Column(db.Integer, db.ForeignKey(ServiceProfessionalInfo.service_professional_id), nullable=False)
    customer_id = db.Column(db.String(36), db.ForeignKey(CustomerInfo.customer_id), nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    customer_rating = db.Column(db.Integer)
    service_professional_remarks = db.Column(db.String(255))