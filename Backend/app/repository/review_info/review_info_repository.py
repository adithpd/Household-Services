from app.models.reviews.reviews_info import ReviewsInfo
from app.models.db import db
from datetime import datetime

class ReviewInfoRepository:
    @staticmethod
    def insert_review_record(review_data):
        review_record = ReviewsInfo(
            service_professional_id=review_data["service_professional_id"],
            booking_id=review_data["booking_id"],
            review_provided="NO",
            currency=review_data["currency"],
            paid_price=review_data["paid_price"],
        )
        db.session.add(review_record)
        db.session.commit()
        return review_record
    
    @staticmethod    
    def fetch_by_booking_id(booking_id):
        review_record = ReviewsInfo.query.filter((ReviewsInfo.booking_id==booking_id)).first()
        return review_record
    
    @staticmethod
    def update_review_info_by_review_id(review_id, review_data):
        review = ReviewsInfo.query.filter_by(review_id=review_id).first()
        review.service_professional_rating = review_data["service_professional_rating"]
        review.review_provided = review_data["review_provided"]
        review.customer_remarks = review_data["customer_remarks"]
        review.paid_price = review_data["paid_price"]
        review.review_given_time = datetime.fromisoformat(review_data["review_given_time"])
        db.session.commit()
        return True