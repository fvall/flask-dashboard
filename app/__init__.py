from flask import Flask
from . import util

def create_app():

    app = Flask(__name__)

    with app.app_context():
        
        from . import index
        return app
