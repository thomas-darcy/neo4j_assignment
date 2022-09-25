from flask import Blueprint, current_app, request, jsonify
from datetime import datetime
from dao.customers import CustomerDAO

customers_routes = Blueprint("customers", __name__, url_prefix="/api/customers")

@customers_routes.route('/create', methods=['POST'])
def create_supplier():
    request_json = request.get_json()

    dao = CustomerDAO(current_app.driver)

    output = dao.create_customers(request_json)

    outputDict = { "recordsSynced": output, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}

    return jsonify(outputDict)

