from ..db import db
import uuid
from sqlalchemy.sql import func


def generate_uuid():
    return uuid.uuid4().hex

class ServiceInfo(db.Model):
    __tablename__ = "service_info"
    service_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    description = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    base_price = db.Column(db.Numeric(10,2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    city = db.Column(db.String(36), nullable=False)
    state = db.Column(db.String(36), nullable=False)
    country = db.Column(db.String(36), nullable=False)
    