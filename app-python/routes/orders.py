from flask import Blueprint, current_app, request, jsonify
from jsonschema import validate
from dao.orders import OrderDAO

orders_routes = Blueprint("orders", __name__, url_prefix="/api/orders")
schema = {
  "type": "array",
  "items": [
    {
      "type": "object",
      "properties": {
        "orderId": {
          "type": "string"
        },
        "customerId": {
          "type": "string"
        },
        "totalValue": {
          "type": "number"
        },
        "shippingName": {
          "type": "string"
        },
        "shippingAddressText": {
          "type": "string"
        },
        "shippingCity": {
          "type": "string"
        },
        "shippingRegion": {
          "type": "string"
        },
        "shippingPostCode": {
          "type": "string"
        },
        "shippingCountry": {
          "type": "string"
        },
        "products": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "productId": {
                  "type": "string"
                },
                "quantity": {
                  "type": "integer"
                },
                "discount": {
                  "type": "number"
                },
                "unitPrice": {
                  "type": "number"
                }
              },
              "required": [
                "productId",
                "quantity",
                "discount",
                "unitPrice"
              ]
            }
          ]
        }
      },
      "required": [
        "orderId",
        "customerId",
        "totalValue",
        "shippingName",
        "shippingAddressText",
        "shippingCity",
        "shippingRegion",
        "shippingPostCode",
        "shippingCountry",
        "products"
      ]
    }
  ]
}

@orders_routes.route('/create', methods=['POST'])
def create_order(movie_id):
    # Get the request payload
    form_data = request.get_json()

    # Validate the input data against the schema
    validate(form_data, schema)

    # get the payload we want
    rating = int(form_data["rating"])

    # Create the DAO
    dao = OrderDAO(current_app.driver)

    # Save the rating
    output = dao.add(movie_id, rating)

    # Return the output
    return jsonify(output)