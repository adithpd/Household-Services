from ..db import db
import uuid
from sqlalchemy.sql import func


def generate_uuid():
    return uuid.uuid4().hex 

class UserInfo(db.Model):
    __tablename__ = "user_info"
    user_id = db.Column(db.String(100), primary_key=True,nullable=False)
    id = db.Column(db.String(36), unique=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    role = db.Column(db.String(50), nullable=False)