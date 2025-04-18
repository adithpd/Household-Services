import jwt
import base64
import io
import zipfile
import time
import PyPDF2
import json
from flask import request, jsonify, current_app, send_file, Response
from app.repository.service_professional.service_professional_documents import ServiceProfessionalDocumentsRepository
from app.repository.service_professional.service_professional_info import ServiceProfessionalRepository
from app.repository.services.service_info_repository import ServiceInfoRepository
from app.repository.request_info.request_info_repository import RequestInfoRepository
from app.repository.customer.customer_repository import CustomerRepository
from app.repository.booking_info.booking_info_repository import BookingInfoRepository
from app.repository.user.user_repository import UserRepository
from app.repository.review_info.review_info_repository import ReviewInfoRepository
from fuzzywuzzy import process
from app import cache, redis_client


MAX_FILE_SIZE = 1 * 1024 * 1024

class ServiceProfessionalService:
    @staticmethod
    def register(service_professional_data):
        if not service_professional_data or not service_professional_data.get('user_id') or not service_professional_data.get('name') or not service_professional_data.get('phone') or not service_professional_data.get('description') or not service_professional_data.get('experience_years') or not service_professional_data.get('location') or not service_professional_data.get('city') or not service_professional_data.get('state') or not service_professional_data.get('country') or not service_professional_data.get('pincode'):
            return jsonify({'message': 'Request does not contain data for required fields'}), 422

        if ServiceProfessionalRepository.fetch_by_user_id(service_professional_data['user_id']):
            return jsonify({'message': 'Request conflicts as Service Professional exists with that username'}), 409
           
        city, state, country = service_professional_data["city"], service_professional_data["state"], service_professional_data["country"]    
        services_in_location = ServiceInfoRepository.fetch_by_location_state_country(city, state, country)
        print(services_in_location)
        service_descriptions = {service.service_id: service.description for service in services_in_location}
        closest_match = process.extractOne(service_professional_data["description"], service_descriptions.values())
        print(closest_match)
        if closest_match:
            matched_service_id = next(sid for sid, desc in service_descriptions.items() if desc == closest_match[0])
            inserted_record = ServiceProfessionalRepository.insert_service_professional_record({
            **service_professional_data,
            "service_id": matched_service_id
            })
        else:
            inserted_record = ServiceProfessionalRepository.insert_service_professional_record(service_professional_data)
        service_professional_id = inserted_record.service_professional_id
        
        cache.delete('service_professional_info')
        
        return jsonify({
            "message": "Service Professional record succesfully inserted!",
            "service_professional_id": service_professional_id
        }), 200
    
    @staticmethod
    def upload_verification_document(service_professional_id, document_data, document_type):
        if not document_data:
            return jsonify({"error": "File not uploaded properly"}), 400
        
        file = next(iter(document_data.values()), None)
        if file is None:
            return jsonify({"error": "No files were uploaded"}), 400
        
        if file.filename == '':
            return jsonify({"error": "No files were uploaded"}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are allowed"}), 400

        valid_types = {"aadhar", "license", "resume"}
        if document_type not in valid_types:
            return jsonify({"error": "Invalid document type. Allowed: [aadhar, license, resume]"}), 400

        document_name = f"{service_professional_id}_{document_type}.pdf"
        
        existing_document = ServiceProfessionalDocumentsRepository.fetch_by_service_professional_id_and_type(service_professional_id, document_type)
        if existing_document:
            return jsonify({"error": f"{document_type} document already exists. Please delete or update it instead"}), 400

        file_data = file.read()
        if len(file_data) > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds 1MB limit"}), 400 

        try:
            pdf_reader = PyPDF2.PdfReader(file)
            if len(pdf_reader.pages) == 0:
                return jsonify({"error": "PDF file is not readable"}), 400
        except Exception:
            return jsonify({"error": "Invalid PDF file"}), 400
        
        new_file = ServiceProfessionalDocumentsRepository.insert_document_record(
            service_professional_id=service_professional_id,
            document_name=document_name,
            document_type=document_type,
            document_data=file_data
        )
        
        cache.delete('service_professional_documents')
        return jsonify({"message": "File uploaded successfully", "file_id": new_file.document_id}), 201\
            
    @staticmethod
    @cache.cached(timeout=60, key_prefix='service_professional_documents')
    def view_verification_document_all(service_professional_id):
        cached_response = redis_client.get('service_professional_documents')
        if cached_response:
          return jsonify(cached_response)

        document_records = ServiceProfessionalDocumentsRepository.fetch_by_service_professional_id(service_professional_id)
        if not document_records:
            return jsonify({"error": "No documents available for verification"}), 404
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for document in document_records:
                try:
                    file_data = document.document_data
                    if not file_data:
                        print(f"Error: File {document.document_name} has no data after decoding.")

                    zip_file.writestr(document.document_name, file_data)

                except Exception as e:
                    print(f"Error decoding {document.document_name}: {e}")
                    return jsonify({"error": f"Failed to process {document.document_name}"}), 500

        zip_buffer.seek(0)
        response = Response(zip_buffer.read(), mimetype="application/zip")
        response.headers["Content-Disposition"] = "attachment; filename=documents.zip"
        
        return response
    
    @staticmethod
    @cache.cached(timeout=60, key_prefix='service_professional_documents')
    def view_verification_document_by_type(service_professional_id, document_type):
        cached_response = redis_client.get('service_professional_documents')
        if cached_response:
          return jsonify(cached_response)
      
        document_records = ServiceProfessionalDocumentsRepository.fetch_by_service_professional_id_and_type(service_professional_id, document_type)
        if not document_records:
            return jsonify({"error": f"{document_type} - document not uploaded"}), 404
        
        document = document_records[0]
        document_name = document.document_name
        file_data = document.document_data
        response = Response(file_data, mimetype="application/pdf")
        response.headers["Content-Disposition"] = f"attachment; filename={document_name}"
        
        return response
    
    @staticmethod
    def update_documents_verified_status(service_professional_id, verified_status):
        update_verified_status = ServiceProfessionalDocumentsRepository.update_verified_by_service_professional_id(service_professional_id, verified_status)
        if not update_verified_status:
            return jsonify({"error": "No documents found for updating verification status"}), 404
        
        cache.delete('service_professional_documents')
        return jsonify({"message": "verification status updated for all documents successfully"}), 200
    
    @staticmethod
    @cache.cached(timeout=60, key_prefix='request_info')
    def view_request_info_live_service_professional(service_professional_data):
        cached_response = redis_client.get('request_info')
        if cached_response:
          return jsonify(cached_response)
      
        user_id = service_professional_data["user_id"]
        professional = ServiceProfessionalRepository.fetch_by_user_id(user_id)
        if not professional:
            return jsonify({"message": "Service Professional not found"}), 404
        service_id = professional[0].service_id
        live_requests = RequestInfoRepository.fetch_live_requests_by_service_id(service_id)
        response_data = []
        for request in live_requests:
            customer_data = CustomerRepository.fetch_by_customer_id(request.customer_id)
            location = "Unknown"
            if customer_data:
                location = customer_data[0].location

            response_data.append({
                "request_id": request.request_id,
                "service_id": request.service_id,
                "customer_id": request.customer_id,
                "start_time": request.start_time.isoformat(),
                "end_time": request.end_time.isoformat(),
                "currency": request.currency,
                "quote_price": request.quote_price,
                "status": request.status,
                "keywords": request.keywords,
                "location": location
            })
        return jsonify({"requests": response_data}), 200
    
    @staticmethod
    def accept_request_info_service_professional(service_professional_data):
        try:
            user_id = service_professional_data["user_id"]
            request_id = service_professional_data["request_id"]

            professional = ServiceProfessionalRepository.fetch_by_user_id(user_id)
            if not professional:
                return jsonify({"message": "Service Professional not found"}), 404

            request_info = RequestInfoRepository.fetch_requests_by_request_id(request_id)
            if not request_info:
                return jsonify({"message": "Request not found"}), 404

            if request_info[0].status != "NEW":
                return jsonify({"message": "Request is no longer available for acceptance"}), 400

            RequestInfoRepository.update_request_status(request_id, "ACCEPTED")

            booking_data = {
                "booking_id": request_info[0].request_id,
                "customer_id": request_info[0].customer_id,
                "service_professional_id": professional[0].service_professional_id,
                "start_time": request_info[0].start_time,
                "end_time": request_info[0].end_time,
                "status": "UPCOMING",
                "currency": request_info[0].currency,
                "price": request_info[0].quote_price,
            }
            BookingInfoRepository.insert_booking_record(booking_data)
            cache.delete('booking_info')
            cache.delete('request_info')
            

            return jsonify({"message": "Request accepted successfully and booking created!"}), 200

        except Exception as e:
            return jsonify({"message": "Error accepting request", "error": str(e)}), 500
        
    @staticmethod
    @cache.cached(timeout=60, key_prefix='booking_info')
    def view_booking_info_service_professional(service_professional_data):
        cached_response = redis_client.get('booking_info')
        if cached_response:
          return jsonify(cached_response)
      
        user_id = service_professional_data["user_id"]
        professional = ServiceProfessionalRepository.fetch_by_user_id(user_id)
        if not professional:
            return jsonify({"message": "Service Professional not found"}), 404
        service_professional_id = professional[0].service_professional_id
        all_bookings = BookingInfoRepository.fetch_booking_info_by_service_professional_id(service_professional_id)
        response_data = []
        for booking in all_bookings:
            request_record = RequestInfoRepository.fetch_accepted_requests_by_request_id(booking.booking_id)
            customer_record = CustomerRepository.fetch_by_customer_id(request_record.customer_id)
            user_record = UserRepository.fetch_by_user_id(customer_record[0].user_id)
            response_data.append({
                "booking_id": booking.booking_id,
                "service_professional_id": booking.service_professional_id,
                "customer_id": booking.customer_id,
                "start_time": booking.start_time.isoformat(),
                "end_time": booking.end_time.isoformat(),
                "currency": booking.currency,
                "price": booking.price,
                "status": booking.status,
                "customer_name": user_record.name,
                "keywords": request_record.keywords,
                "service_professional_remarks": booking.service_professional_remarks,
                "customer_rating": booking.customer_rating,
            })
        return jsonify({"requests": response_data}), 200
    
    @staticmethod
    def cancel_booking_info_service_professional(booking_data):
        try:
            booking_id = booking_data["booking_id"]
            print(booking_id)
            BookingInfoRepository.delete_by_booking_id(booking_id)
            RequestInfoRepository.delete_by_request_id(booking_id)
            cache.delete('booking_info')
            return jsonify({"message": "Booking has been sucessfully cancelled"}), 200
        except Exception as e:
            return jsonify({"message": "Error cancelling booking", "error": str(e)}), 500

    @staticmethod
    def mark_completed_booking_info_service_professional(booking_data):
        try:
            user_id = booking_data["user_id"]
            booking_id = booking_data["booking_id"]
            service_professional_remarks = booking_data["remarks"]
            customer_rating = booking_data["rating"]
            BookingInfoRepository.mark_complete_by_booking_id(booking_id, service_professional_remarks, customer_rating)
            booking_record = BookingInfoRepository.fetch_booking_info_by_booking_id(booking_id)
            service_professional_record = ServiceProfessionalRepository.fetch_by_user_id(user_id)
            review_data = {
                "service_professional_id": service_professional_record[0].service_professional_id,
                "booking_id": booking_id,
                "currency": booking_record[0].currency,
                "paid_price": booking_record[0].price, 
            }
            ReviewInfoRepository.insert_review_record(review_data)
            cache.delete('review_info')
            return jsonify({"message": "Booking has been marked as completed sucessfully"}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Error marking booking as completed", "error": str(e)}), 500
    
    @staticmethod
    @cache.cached(timeout=60, key_prefix='review_info')
    def view_review_info_service_professional(service_professional_data):
        cached_response = redis_client.get('review_info')
        if cached_response:
          return jsonify(cached_response)
      
        user_id = service_professional_data["user_id"]
        professional = ServiceProfessionalRepository.fetch_by_user_id(user_id)
        if not professional:
            return jsonify({"message": "Service Professional not found"}), 404
        service_professional_id = professional[0].service_professional_id
        all_bookings = BookingInfoRepository.fetch_booking_info_by_service_professional_id_completed(service_professional_id)
        response_data = []
        for booking in all_bookings:
            request_record = RequestInfoRepository.fetch_accepted_requests_by_request_id(booking.booking_id)
            customer_record = CustomerRepository.fetch_by_customer_id(request_record.customer_id)
            user_record = UserRepository.fetch_by_user_id(customer_record[0].user_id)
            review_record = ReviewInfoRepository.fetch_by_booking_id(booking.booking_id)
            if review_record.review_provided == "YES":
                response_data.append({
                    "booking_id": booking.booking_id,
                    "start_time": booking.start_time.isoformat(),
                    "end_time": booking.end_time.isoformat(),
                    "currency": booking.currency,
                    "price": review_record.paid_price,
                    "customer_name": user_record.name,
                    "keywords": request_record.keywords,
                    "customer_review": review_record.customer_remarks,
                    "customer_rating": review_record.service_professional_rating,
                })
        return jsonify({"reviews": response_data}), 200

    def download_report_service_professional(user_id):
        from app.celery_jobs.celery_tasks import export_service_requests
        service_professional_record = ServiceProfessionalRepository.fetch_by_user_id(user_id)
        service_professional_id = service_professional_record[0].service_professional_id
        if not service_professional_id:
            return jsonify({"error": "Service Professional ID is required"}), 400
        
        task = export_service_requests.apply_async(args=[service_professional_id])
        return jsonify({"message": "Export initiated", "task_id": task.id}), 202
    
    def fetch_verified_by_user_id(user_id):
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        service_professional = ServiceProfessionalRepository.fetch_by_user_id(user_id)[0]
        if not service_professional:
            return jsonify({"error": "User not found"}), 404

        service_professional_documents = ServiceProfessionalDocumentsRepository.fetch_by_service_professional_id(service_professional.service_professional_id)
        for document in service_professional_documents:
            if document.verified == "NOT VERIFIED":
                return jsonify({"verified": "NOT VERIFIED"}), 200

        return jsonify({"verified": "VERIFIED"}), 200