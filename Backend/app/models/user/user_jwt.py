from ..db import db
import uuid
from sqlalchemy.sql import func
from ..user.user_info import UserInfo


def generate_uuid():
    return uuid.uuid4().hex 

class UserJWT(db.Model):
    __tablename__ = "user_jwt"
    user_id = db.Column(db.String(100), db.ForeignKey(UserInfo.user_id), primary_key=True, nullable=False)
    jwt = db.Column(db.String(500), nullable=False)
    last_logged_in = db.Column(db.TIMESTAMP, server_default=func.current_timestamp(), nullable=False)