from ..db import db
import uuid
from sqlalchemy.sql import func
from ..user.user_info import UserInfo

def generate_uuid():
    return uuid.uuid4().hex

class CustomerInfo(db.Model):
    __tablename__ = "customer_info"
    customer_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(100), db.ForeignKey(UserInfo.user_id), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    phone = db.Column(db.String(20), nullable=False, unique=True)
    blocked = db.Column(db.String(20), nullable=False, default='Not Blocked')