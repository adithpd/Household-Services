from app.models.service_professional.service_professional_documents import ServiceProfessionalDocuments
from app.models.db import db

class ServiceProfessionalDocumentsRepository:
    @staticmethod
    def insert_document_record(service_professional_id,document_name,document_type,document_data):
        document_record = ServiceProfessionalDocuments(
            service_professional_id=service_professional_id,
            document_name=document_name, 
            document_type=document_type,
            document_data=document_data
        )
        db.session.add(document_record)
        db.session.commit()
        return document_record
    
    @staticmethod
    def fetch_by_service_professional_id(service_professional_id):
        document_records = ServiceProfessionalDocuments.query.filter((ServiceProfessionalDocuments.service_professional_id==service_professional_id)).all()
        return document_records
    
    @staticmethod
    def fetch_by_service_professional_id_and_type(service_professional_id,document_type):
        document_record = ServiceProfessionalDocuments.query.filter((ServiceProfessionalDocuments.service_professional_id==service_professional_id) & (ServiceProfessionalDocuments.document_type==document_type)).all()
        return document_record
    
    @staticmethod
    def update_verified_by_service_professional_id(service_professional_id, verified_status):
        document_records = ServiceProfessionalDocuments.query.filter((ServiceProfessionalDocuments.service_professional_id==service_professional_id)).all()
        if not document_records:
            return False
        
        for document in document_records:
            document.verified = verified_status
        
        db.session.commit()
        return True