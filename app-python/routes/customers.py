from flask import Blueprint, current_app, request, jsonify
from jsonschema import validate

from dao.customers import CustomerDAO

customers_routes = Blueprint("customers", __name__, url_prefix="/api/customers")
schema = {
   "type":"array",
   "items":[
      {
         "type":"object",
         "properties":{
            "customerId":{
               "type":"string"
            },
            "companyName":{
               "type":"string"
            },
            "contactName":{
               "type":"string"
            },
            "contactRole":{
               "type":"string"
            },
            "addressText":{
               "type":"string"
            },
            "city":{
               "type":"string"
            },
            "region":{
               "type":[
                  "string",
                  "null"
               ]
            },
            "postCode":{
               "type":[
                  "string",
                  "null"
               ]
            },
            "country":{
               "type":"string"
            }
         },
         "required":[
            "customerId",
            "companyName",
            "contactName",
            "contactRole",
            "addressText",
            "city",
            "country"
         ]
      }
   ]
}

@customers_routes.route('/create', methods=['POST'])
def create_supplier():
    # Get the request payload
    request_json = request.get_json()

   #  # Validate the input data against the schema
   #  validate(request_json, schema)

    # Create the DAO
    dao = CustomerDAO(current_app.driver)

    # Save the rating
    output = dao.create_customers(request_json)

    # Return the output
    return jsonify(output)

