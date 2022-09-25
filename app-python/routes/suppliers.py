from flask import Blueprint, current_app, request, jsonify
from jsonschema import validate
from dao.suppliers import SupplierDAO

suppliers_routes = Blueprint("suppliers", __name__, url_prefix="/api/suppliers")
schema = {
  "type": "array",
  "items": [
    {
      "type": "object",
      "properties": {
        "supplierId": {
          "type": "string"
        },
        "companyName": {
          "type": "string"
        },
        "contactName": {
          "type": "string"
        },
        "contactRole": {
          "type": "string"
        },
        "addressText": {
          "type": "string"
        },
        "city": {
          "type": "string"
        },
        "region": {
          "type": ["string","null"]
        },
        "postCode": {
          "type": ["string","null"]
        },
        "country": {
          "type": "string"
        }
      },
      "required": [
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
def create_supplier(movie_id):
    # Get the request payload
    form_data = request.get_json()

    # Validate the input data against the schema
    validate(form_data, schema)

    ## get the payload we want
    rating = int(form_data["rating"])

    # Create the DAO
    dao = SupplierDAO(current_app.driver)

    # Save the rating
    output = dao.add(movie_id, rating)

    # Return the output
    return jsonify(output)

