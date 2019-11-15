from flask import request
from flask_restplus import Resource

from ..utils.dto import ContractDto
from ..services.contract_service import create_contract, get_all_contracts, get_contracts_in_progress, get_a_contract

api = ContractDto.api
_contract = ContractDto.contract



@api.route('/', methods=['GET'])
class ContractList(Resource):
    @api.doc('List of contracts')
    @api.marshal_list_with(_contract, envelope='data')
    def get(self,in_progress=False):
        """List all registered users"""
        print('get_user')
        if in_progress:
            return get_contracts_in_progress()
        return get_all_contracts()


@api.route('/<address>', methods=['GET'])
@api.param('address', 'The Contract identifier')
@api.response(404, 'Contract not found.')
class Contract(Resource):
    @api.doc('get a contract')
    @api.marshal_with(_contract)
    def get(self, address):
        """Get contract with his identifier"""
        print('get_a_contract')
        contract = get_a_contract(address)
        if not contract:
            api.abort(404)
        else:
            return contract


@api.route('/create', methods=['POST'])
class ContractCreate(Resource):
    @api.response(201, 'Contract successfully created.')
    @api.doc('Create a new contract')
    @api.expect(_contract, validate=True)
    def post(self):
        """Create a new contract """
        print('post_contract')
        data = request.json
        return create_contract(data=data)