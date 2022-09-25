import os

from flask import Flask

from exceptions.notfound import NotFoundException
from exceptions.badrequest import BadRequestException

from neo4j import init_driver

from routes.orders import orders_routes
from routes.suppliers import suppliers_routes
from routes.customers import customers_routes

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__)

    app.config.from_mapping(
        NEO4J_URI=os.getenv('NEO4J_URI'),
        NEO4J_USERNAME=os.getenv('NEO4J_USERNAME'),
        NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD'),
        NEO4J_DATABASE=os.getenv('NEO4J_DATABASE'),
    )

    # Apply Test Config
    if test_config is not None:
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        init_driver(
            app.config.get('NEO4J_URI'),
            app.config.get('NEO4J_USERNAME'),
            app.config.get('NEO4J_PASSWORD'),
        )

    # Register Routes
    app.register_blueprint(orders_routes)
    app.register_blueprint(customers_routes)
    app.register_blueprint(suppliers_routes)

    @app.errorhandler(BadRequestException)
    def handle_bad_request(err):
        return {"message": str(err)}, 400

    @app.errorhandler(NotFoundException)
    def handle_not_found_exception(err):
        return {"message": str(err)}, 404

    return app


app = create_app()