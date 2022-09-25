from flask import Flask, current_app
from neo4j import GraphDatabase

def init_driver(uri, username, password):
    # Create an instance of the driver
    current_app.driver = GraphDatabase.driver(uri, auth=(username, password))

    # Verify Connectivity
    current_app.driver.verify_connectivity()

    return current_app.driver


def get_driver():
    return current_app.driver


def close_driver():
    if current_app.driver != None:
        current_app.driver.close()
        current_app.driver = None

        return current_app.driver
