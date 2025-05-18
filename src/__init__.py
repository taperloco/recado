from flask import Flask
from flask_restful import Api
from src.controllers.controller import Controller


def create_app():
    # Create app and api
    app = Flask(__name__)
    api = Api(app)
    
    # Endpoints
    api.add_resource(Controller, 
                     '/recado/recados',
                     '/recado/chats',
                     '/recado/update',
                     

                     '/recado/login',
                     '/recado/register',
                     '/recado/token',
                     '/recado/update',

                     '/recado/getchat',
                     )
    return app




