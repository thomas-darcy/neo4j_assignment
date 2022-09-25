from flask import Blueprint, current_app, request, jsonify
from jsonschema import validate

from dao.customers import CustomerDAO

customers_routes = Blueprint("customers", __name__, url_prefix="/api/customers")
schema = {
  "type": "array",
  "items": [
    {
      "type": "object",
      "properties": {
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
def create_supplier(movie_id):
    # Get the request payload
    form_data = request.get_json()

    # Validate the input data against the schema
    validate(form_data, schema)

    ## get the payload in the format we want
    rating = int(form_data["rating"])

    # Create the DAO
    dao = CustomerDAO(current_app.driver)

    # Save the rating
    output = dao.add(movie_id, rating)

    # Return the output
    return jsonify(output)

