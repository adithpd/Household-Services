from ..db import db
import uuid
from sqlalchemy.sql import func
from ..service_professional.service_professional_info import ServiceProfessionalInfo
from ..booking.booking_info import BookingInfo


def generate_uuid():
    return uuid.uuid4().hex

class ReviewsInfo(db.Model):
    __tablename__ = "reviews_info"
    review_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    service_professional_id = db.Column(db.String(36), db.ForeignKey(ServiceProfessionalInfo.service_professional_id), nullable=False)
    booking_id = db.Column(db.String(36), db.ForeignKey(BookingInfo.booking_id), nullable=False)
    service_professional_rating = db.Column(db.Integer)
    review_provided = db.Column(db.String(500), nullable=False)
    customer_remarks = db.Column(db.String(255))
    currency = db.Column(db.String(10), nullable=False)
    paid_price = db.Column(db.Numeric(10,2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    review_given_time = db.Column(db.TIMESTAMP)