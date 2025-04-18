from ..db import db
import uuid
from sqlalchemy.sql import func
from ..services.service_info import ServiceInfo
from ..user.user_info import UserInfo


def generate_uuid():
    return uuid.uuid4().hex 

class ServiceProfessionalInfo(db.Model):
    __tablename__ = "service_professional_info"
    service_professional_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(100), db.ForeignKey(UserInfo.user_id), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    description = db.Column(db.String(255), nullable=False)
    service_keywords = db.Column(db.JSON, nullable=True)
    service_id = db.Column(db.String(36), nullable=True)
    experience_years = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    record_status=db.Column(db.String(20), nullable=False, default='U')
    
    def __repr__(self):
        return (
            f"<ServiceProfessionalInfo("
            f"id={self.service_professional_id}, user_id={self.user_id}, name={self.name}, phone={self.phone}, "
            f"created_at={self.created_at}, description={self.description}, keywords={self.service_keywords}, "
            f"service_id={self.service_id}, experience={self.experience_years} years, location={self.location}, "
            f"city={self.city}, state={self.state}, country={self.country}, pincode={self.pincode}, "
            f"record_status={self.record_status})>"
        )