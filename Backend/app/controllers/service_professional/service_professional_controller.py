from flask import request, jsonify, current_app, send_from_directory
from app.services.service_professional.service_professional_service import ServiceProfessionalService
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery.result import AsyncResult
from werkzeug.utils import safe_join
import os


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["500 per day", "100 per hour"]
)


def service_professional_routes(app):
    limiter.init_app(app)
    
    @app.route('/service-professional/register', methods=['POST'])
    @limiter.limit("5 per minute")
    def service_professional_insert():
        service_professional_data = request.json
        return ServiceProfessionalService.register(service_professional_data)
    
    @app.route('/sp/verification/document/upload', methods=['POST'])
    @limiter.limit("3 per minute")
    def upload_verification_document():
        service_professional_id = request.form.get("service_professional_id")
        document_type = request.form.get("document_type")
        document_data = request.files
        return ServiceProfessionalService.upload_verification_document(service_professional_id, document_data, document_type)
    
    @app.route('/sp/verification/document/view/all', methods=['GET'])
    @limiter.limit("20 per minute")
    def view_verification_document_all():
        service_professional_id = request.args.get("service_professional_id")
        return ServiceProfessionalService.view_verification_document_all(service_professional_id)
    
    @app.route('/sp/verification/document/view/type', methods=['GET'])
    @limiter.limit("20 per minute")
    def view_verification_document_by_type():
        service_professional_id = request.args.get("service_professional_id")
        document_type = request.args.get("document_type")
        return ServiceProfessionalService.view_verification_document_by_type(service_professional_id, document_type)
    
    @app.route('/sp/verification/document/verified', methods=['GET'])
    @limiter.limit("50 per minute")
    def update_documents_verification_status():
        service_professional_id = request.args.get("service_professional_id")
        verified_status = request.args.get("verified_status")
        return ServiceProfessionalService.update_documents_verified_status(service_professional_id, verified_status)
    
    @app.route('/sp/request-info/view', methods=['POST'])
    @limiter.limit("30 per minute")
    def view_request_info_live_service_professional():
        service_professional_data = request.json
        return ServiceProfessionalService.view_request_info_live_service_professional(service_professional_data)
    
    @app.route('/sp/request-info/accept', methods=['POST'])
    @limiter.limit("50 per minute")
    def accept_request_info_service_professional():
        service_professional_data = request.json
        return ServiceProfessionalService.accept_request_info_service_professional(service_professional_data)
    
    @app.route('/sp/booking-info/view', methods=['POST'])
    @limiter.limit("10 per minute")
    def view_booking_info_service_professional():
        service_professional_data = request.json
        return ServiceProfessionalService.view_booking_info_service_professional(service_professional_data)
    
    @app.route('/sp/booking-info/cancel', methods=['POST'])
    @limiter.limit("10 per minute")
    def cancel_booking_info_service_professional():
        booking_data = request.json
        return ServiceProfessionalService.cancel_booking_info_service_professional(booking_data)
    
    @app.route('/sp/booking-info/completed', methods=['POST'])
    @limiter.limit("10 per minute")
    def mark_completed_booking_info_service_professional():
        booking_data = request.json
        return ServiceProfessionalService.mark_completed_booking_info_service_professional(booking_data)
    
    @app.route('/sp/review-info/view', methods=['POST'])
    @limiter.limit("30 per minute")
    def view_review_info_service_professional():
        service_professional_data = request.json
        return ServiceProfessionalService.view_review_info_service_professional(service_professional_data)
    
    @app.route("/export/service-requests", methods=["POST"])
    @limiter.limit("5 per minute")
    def export_requests():
        data = request.json
        user_id = data.get("user_id")
        return ServiceProfessionalService.download_report_service_professional(user_id)
    
    @app.route("/celery/status/<task_id>", methods=["GET"])
    @limiter.limit("50 per minute")
    def get_task_status(task_id):
        task_result = AsyncResult(task_id, app=current_app.extensions["celery"])
        if task_result.state == "PENDING":
            response = {"status": "pending"}
        elif task_result.state == "SUCCESS":
            if task_result.result and isinstance(task_result.result, dict):
                file_url = task_result.result.get("file_url", "")
            else:
                file_url = ""

            response = {
                "status": "success",
                "file_url": file_url
            }
        elif task_result.state == "FAILURE":
            error_message = str(task_result.result) if task_result.result else "Unknown error occurred."
            response = {
                "status": "failed",
                "error": error_message
            }
        else:
            response = {"status": task_result.state}

        return jsonify(response)
    
    @app.route("/reports/<filename>")
    @limiter.limit("50 per minute")
    def download_report(filename):
        report_folder = os.path.abspath(os.path.join(os.getcwd(), "report_generated"))
        file_path = safe_join(report_folder, filename)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return jsonify({"error": "File not found"}), 404

        print(f"Serving file: {file_path}")
        return send_from_directory(report_folder, filename, as_attachment=True)
    
    @app.route("/service-professional/verify-status", methods=["GET"])
    def verify_status_service_professional():
        user_id = request.args.get("user_id")
        return ServiceProfessionalService.fetch_verified_by_user_id(user_id)
        
        