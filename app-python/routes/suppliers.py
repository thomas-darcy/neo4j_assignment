from flask import Blueprint, current_app, request, jsonify
from datetime import datetime
from dao.suppliers import SupplierDAO

suppliers_routes = Blueprint("suppliers", __name__, url_prefix="/api/suppliers")


@suppliers_routes.route('/create', methods=['POST'])
def create_supplier():
    request_json = request.get_json()

    dao = SupplierDAO(current_app.driver)

    output = dao.create_suppliers(request_json)

    outputDict = { "recordsSynced": output, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}

    return jsonify(outputDict)

