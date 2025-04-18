from app.models.user.user_info import UserInfo
from app.models.db import db


class UserRepository:
    @staticmethod
    def insert_user_record(registry_data):
        user_record = UserInfo(user_id=registry_data['user_id'], name=registry_data['name'], email=registry_data['email'], password=registry_data['password'], role=registry_data['role'])
        db.session.add(user_record)
        db.session.commit()
        return user_record
    
    @staticmethod
    def fetch_by_user_id(user_id):
        user_record = UserInfo.query.filter((UserInfo.user_id == user_id)).first()
        return user_record
    
    @staticmethod
    def fetch_by_email_id(email):
        user_record = UserInfo.query.filter((UserInfo.email == email)).first()
        return user_record
    
    @staticmethod
    def update_email(user_id, new_email):
        user_record = UserInfo.query.filter_by(user_id=user_id).first()
        if user_record:
            user_record.email = new_email
            db.session.commit()
            return user_record
        return None

    @staticmethod
    def update_password(user_id, new_password):
        user_record = UserInfo.query.filter_by(user_id=user_id).first()
        if user_record:
            user_record.password = new_password
            db.session.commit()
            return user_record
        return None