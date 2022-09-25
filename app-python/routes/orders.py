from flask import Blueprint, current_app, request, jsonify
from datetime import datetime
from dao.orders import OrderDAO

orders_routes = Blueprint("orders", __name__, url_prefix="/api/orders")

@orders_routes.route('/create', methods=['POST'])
def create_order():
    request_json = request.get_json()

    dao = OrderDAO(current_app.driver)

    output = dao.create_orders(request_json)

    outputDict = { "recordsSynced": output, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}

    return jsonify(outputDict)