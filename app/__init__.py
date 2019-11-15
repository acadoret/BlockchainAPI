from flask_restplus import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_ns
from .main.controllers.contract_controller import api as contract_ns


blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='BlockchainAPI for eth',
    version='1.0',
    description='Flask RESTPlus web service for manage and interact with specified contract on ETH Blockchain'
)

api.add_namespace(user_ns, path='/users')
api.add_namespace(contract_ns, path='/contracts')

