from ..db import db
import uuid
from sqlalchemy.sql import func
from ..service_professional.service_professional_info import ServiceProfessionalInfo

def generate_uuid():
    return uuid.uuid4().hex 

class ServiceProfessionalDocuments(db.Model):
    __tablename__ = 'service_professional_documents'

    document_id = db.Column(db.String, primary_key=True, default=generate_uuid)
    service_professional_id = db.Column(db.String, db.ForeignKey(ServiceProfessionalInfo.service_professional_id), nullable=False)
    document_name = db.Column(db.String, nullable=False)
    document_type = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    verified = db.Column(db.String, default="NOT VERIFIED")
    document_data = db.Column(db.LargeBinary, nullable=False)