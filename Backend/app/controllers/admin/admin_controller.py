from flask import request, jsonify
from app.services.admin.admin_service import AdminService
from app.services.authentication.auth_service import AuthService
from flask import jsonify, request


def admin_routes(app):
    @app.route('/admin/create/service', methods=['POST'])
    def create_service():
        service_data = request.json
        return AdminService.create_service(service_data)
    
    @app.route('/admin/service-professional/verification/data', methods=['GET'])
    def service_professional_verification_data():
        return AdminService.service_professional_verification_data()
    
    @app.route('/admin/customer/data', methods=['GET'])
    def customer_data():
        return AdminService.customer_data()
    
    @app.route('/admin/service-info/data', methods=['GET'])
    def service_info_data():
        return AdminService.service_info_data()
    
    @app.route('/admin/service-info/delete', methods=['DELETE'])
    def service_info_delete():
        service_data = request.json
        return AdminService.service_info_delete(service_data)
    
    @app.route('/admin/service-info/edit', methods=['PATCH'])
    def service_info_edit():
        service_data = request.json
        print(service_data)
        return AdminService.service_info_edit(service_data)