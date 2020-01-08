from flask import request
from flask_restplus import Resource

from app.main.utils.dto import ContractDto
from app.main.services.contract_service import create_contract, get_all_contracts, get_contracts_in_progress, get_a_contract, send_vote
from app.main.utils.decorators import admin_token_required, token_required
api = ContractDto.api
_contract = ContractDto.contract



@api.route('/all', methods=['GET'])
class ContractList(Resource):
    @api.doc('List of contracts')
    @api.marshal_list_with(_contract, mask='user_address', envelope='data')
    def get(self,in_progress=False):
        """List all registered contracts"""
        print('get_user')
        if in_progress:
            return get_contracts_in_progress()
        return get_all_contracts()


@api.route('/<address>', methods=['GET'])
@api.param('address', 'The Contract identifier')
@api.response(404, 'Contract not found.')
class Contract(Resource):
    @api.doc('Get a contract')
    @api.marshal_with(_contract)
    def get(self, address):
        """Get contract with his identifier"""
        print('get_a_contract')
        contract = get_a_contract(address)
        if not contract:
            api.abort(404)
        else:
            return contract


    @api.response(201, 'Your vote has been saved.')
    @api.doc('Vote for a proposal')
    @api.expect(_contract, validate=True)
    def post(self,contract_address, proposal_address):
        print('vote for proposal')
        return send_vote(data=request.json)

@api.route('/create', methods=['POST'])
class ContractCreate(Resource):
    @api.response(201, 'Contract successfully created.')
    @api.doc('Create a new contract')
    @api.expect(_contract, validate=True)
    # @token_required
    def post(self):
        """Create a new contract """
        print('post_contract')
        return create_contract(data=request.json)