from app.models.customer.customer_info import CustomerInfo
from app.models.db import db

class CustomerRepository:
    @staticmethod
    def insert_customer_record(customer_data):
        customer_record = CustomerInfo(
            user_id=customer_data["user_id"],
            location=customer_data["location"], 
            city=customer_data["city"],
            state=customer_data["state"],
            country=customer_data["country"],
            pincode=customer_data["pincode"],
            phone=customer_data["phone"]
        )
        db.session.add(customer_record)
        db.session.commit()
        return customer_record
    
    @staticmethod    
    def fetch_by_user_id(user_id):
        customer_record = CustomerInfo.query.filter((CustomerInfo.user_id==user_id)).all()
        return customer_record
    
    @staticmethod    
    def fetch_by_customer_id(customer_id):
        customer_record = CustomerInfo.query.filter((CustomerInfo.customer_id==customer_id)).all()
        return customer_record
    
    @staticmethod
    def update_blocked_by_customer_id(customer_id, blocked):
        customer_record = CustomerInfo.query.filter((CustomerInfo.customer_id==customer_id)).all()
        if not customer_record:
            return False
        
        for customer in customer_record:
            customer.blocked = blocked
        
        db.session.commit()
        return True