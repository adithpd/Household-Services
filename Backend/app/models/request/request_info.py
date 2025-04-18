from ..db import db
import uuid
from sqlalchemy.sql import func
from ..customer.customer_info import CustomerInfo
from ..services.service_info import ServiceInfo


def generate_uuid():
    return uuid.uuid4().hex

class RequestInfo(db.Model):
    __tablename__ = "request_info"
    request_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    customer_id = db.Column(db.Integer, db.ForeignKey(CustomerInfo.customer_id), nullable=False)
    keywords = db.Column(db.JSON, nullable=False)
    service_id = db.Column(db.String(36), db.ForeignKey(ServiceInfo.service_id))
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    quote_price = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    
    def to_dict(self):
        return {
            "request_id": self.request_id,
            "customer_id": self.customer_id,
            "keywords": self.keywords,
            "service_id": self.service_id,
            "start_time": self.start_time.isoformat(),  
            "end_time": self.end_time.isoformat(),
            "currency": self.currency,
            "quote_price": str(self.quote_price),
            "status": self.status,
        }
