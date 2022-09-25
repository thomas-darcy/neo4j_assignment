import os

import pytest
from dotenv import load_dotenv

from app import create_app
from neo4jdriver import init_driver, close_driver

# From GraphAcademy example project

@pytest.fixture(scope = 'session', autouse = True)
def load_env():
   load_dotenv()


@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            init_driver(
                os.environ.get('NEO4J_URI'),
                os.environ.get('NEO4J_USERNAME'),
                os.environ.get('NEO4J_PASSWORD'),
            )
        yield client
