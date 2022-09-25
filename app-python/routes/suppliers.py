from flask import Blueprint, current_app, request, jsonify
from jsonschema import validate
from dao.suppliers import SupplierDAO

suppliers_routes = Blueprint("suppliers", __name__, url_prefix="/api/suppliers")
schema = {
   "type":"array",
   "items":[
      {
         "type":"object",
         "properties":{
            "supplierId":{
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
            "supplierId",
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


@suppliers_routes.route('/create', methods=['POST'])
def create_supplier():
    # Get the request payload
    request_json = request.get_json()

   #  # Validate the input data against the schema
   #  validate(request_json, schema)

    # Create the DAO
    dao = SupplierDAO(current_app.driver)

    # Save the rating
    output = dao.create_supplier(request_json)

    # Return the output
    return jsonify(output)

