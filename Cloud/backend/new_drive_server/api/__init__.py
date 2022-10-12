from flask import Blueprint
from .storage import initialize_storage
from .info import initialize_info

def create_api():
    app = Blueprint("api", __name__)
    initialize_storage(app)
    initialize_info(app)
    return app
