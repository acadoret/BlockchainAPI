from flask_restplus import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='FLASK RESTPLUS TEST JWT',
    version='1.0',
    description='Test for flask restplus web service'
)

api.add_namespace(user_ns, path='/users')

