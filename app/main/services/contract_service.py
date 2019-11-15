import json
import ntpath
from datetime import datetime
from os import urandom

from app.main import db
from app.main.models.contract import Contract, ContractEncoder
from app.main.models.proposal import Proposal
from app.main.models.user import User

from ..utils.blockchain_utils import web3

date_format = "%d/%m/%Y"

def save_changes(data):
    print('save_changes')
    db.session.add(data)
    db.session.commit()

def get_contract(_tx_hash, _abi):
    print('get_contract')
    tx_receipt = web3.eth.waitForTransactionReceipt(_tx_hash)
    return web3.eth.contract(
        address = tx_receipt.contractAddress,
        abi = _abi
    )

def get_a_contract(data):
    print('get_a_contract')
    if data.get('address'):
        return Contract.query.filter_by(address=data.get('address')).first()
    else:
        return Contract.query.filter_by(address=data.get('name'))

def get_all_contracts():
    print('get_all_contracts')
    return Contract.query.all()

def get_contracts_in_progress():
    print('get_contracts_in_prograss')
    return Contract.query.filter(
        Contract.end_date > datetime.now().strftime(date_format)
    ).first_or_404(description = 'There is no contract in progress')

def save_new_contract(data):
    print('save_new_contract')
    # Instanciate new contract
    new_contract = Contract(
        address = data.get('contractAddress'), 
        name = data.get('name'), 
        description = data.get('descripiton'),
        end_date = datetime.strptime(data.get('end_date'), date_format),
        user_id = data.get('user').get('address')
    )
    # Store contract to database
    save_changes(new_contract)
    return new_contract

def create_contract(data):
    print('create_contract')
    user = data.get('user')
    if user:
        eth = web3.eth
        tx_receipt, contract = None

        stored_contract = Contract(
            name = data.get('name'), 
            description = data.get('descripiton'),
            end_date = datetime.strptime(data.get('end_date'), date_format),
            user_id = data.get('user').get('address')
        )

        ballot = eth.contract(abi=stored_contract.abi,bytecode=stored_contract.bytecode)   

        if data.get('proposals'): 

            for prop in data.get('proposals'):
                # Instanciate new Proposal object
                proposal = Proposal(
                    _name = bytes(prop.get('name'),'utf-8'),
                    _address = web3.toChecksumAddress(prop.get('address'))
                )
                stored_contract.proposalNames.append(proposal.name)
                stored_contract.proposalAddrs.append(proposal.address)
            
            try:
                # If the Blockchain does not responding, we return 401 HTTP code  
                tx_hash = ballot.constructor(
                    stored_contract.proposalNames,
                    stored_contract.proposalAddrs
                ).transact()

                ethereum_contract = get_contract(tx_hash=tx_hash, abi=stored_contract.abi)
                stored_contract.address = ethereum_contract.address

            except:
                return {
                    'status': 'Transaction failed',
                    'message': 'Connection with Blockchain can\'t be established '
                }, 401
            
                # Store contract to database
                save_changes(stored_contract) 

            # Return 201 HTTP code
            return {
                'status': 'success',
                'message': 'Ballot successfully registered.',
                'contract' : json.dumps(stored_contract, cls=ContractEncoder)
            }, 201


        # Return 400 HTTP code when proposals does not filled
        return {
            'status': 'fail',
            'message': 'Proposals data doesn\'t filled correctly. Please try again.'
        }, 400
    # Return 401 HTTP code when any user does not connected 
    return {
        'status': 'fail',
        'message': 'Unauthorized user.'
    }, 401

def resgister_on_vote(data):
    if data.get('user'):
        return True

def send_vote(data):
    if data.get('user'):
        if data.get('contract_address'):
            contract = Contract.query.filter_by(
                address = data.get('contract_address')
            ).first_or_404(description = 'Ballot not found')
            
            contract_address = web3.toChecksumAddress(data.get('contract_address'))

        return {
            'status' : 'fail',
            'message': 'You should vote for a contract.'
        }, 400

    return {
        'status': 'fail',
        'message': 'Unauthorized user.'
    }, 401