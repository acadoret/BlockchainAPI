import json
import ntpath
from datetime import datetime
from os import urandom

from app.main import db
from app.main.models.contract import Contract, ContractEncoder
from app.main.models.proposal import Proposal, ProposalEncoder
from app.main.models.user import User
from .user_service import get_all_users

from ..utils.blockchain_utils import web3

date_format = "%d/%m/%Y"

def save_changes(data):
    print('save_changes')
    db.session.add(data)
    db.session.commit()

def get_contract_from_blocks(_contract):
    ''' Get contract from blockchain '''
    try:
        return web3.eth.contract(
            address = web3.toChecksumAddress(_contract.address),
            abi = _contract.abi
        )
    except:
        return {
            'status': 'Transaction failed',
            'message': 'Connection with Blockchain can\'t be established. The contract cannot be fetched.'
        }, 401
 
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

def create_contract_to_blocks(_contract):
    try:
        # If the Blockchain does not responding, we return 401 HTTP code 
        
        Ballot = web3.eth.contract(abi=_contract._abi,bytecode=_contract._bytecode)       
        # DECRYPT AND GET PRIVATEKEY
        # GET USER
        user = User.query.filter_by(address=_contract.user_id).first() 
        # RETRIEVE PKEY
        private_key = web3.eth.account.decrypt(user.keystore, user.password) 
        # GET ACCOUNT WITH PKEY
        eth_account = web3.eth.account.privateKeyToAccount(private_key) 

        tx = Ballot.constructor().buildTransaction({
            'from': eth_account.address,
            'nonce': web3.eth.getTransactionCount(eth_account.address)
        })

        signed = eth_account.signTransaction(tx)

        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
    
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt["contractAddress"]
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=_contract._abi)
        print("contract")
        print(contract.address)
        print("Contract address : {}".format(contract_address))
        print("ACCOUNT ADDRESS : {} \n\r".format(eth_account.address))

        for proposal in _contract._proposals:
            print("GAS ESTIMATION : {} \n\r".format(contract.functions.addCandidate(proposal.name).estimateGas()))
            # print("NB PROP : {} \n\r".format(contract.functions.candidateCount().call()))
            print("proposal")
            print(proposal)
            tx = contract.functions.addCandidate(proposal.name).buildTransaction({
                'from': eth_account.address,
                'nonce': web3.eth.getTransactionCount(eth_account.address)
            })
            signed = eth_account.signTransaction(tx)
            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
            _tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            print("_tx_receipt")
            print(_tx_receipt)
            
        return contract_address

    except:
        return {
            'status': 'Transaction failed',
            'message': 'Connection with Blockchain can\'t be established. The contract cannot be created '
        }, 401

def create_contract(data):
    print('create_contract')
    user = data.get('user')
    if user:
        if data.get('proposals'): 
            eth = web3.eth
            tx_receipt = None
            contract = None
            stored_contract = Contract(
                name = data.get('name'), 
                description = data.get('descripiton'),
                end_date = datetime.strptime(data.get('end_date'), date_format),
                user_id = data.get('address')
            )
            props = json.loads(data.get('proposals'))
            for prop in props:
                # Instanciate new Proposal object
                proposal = Proposal(_name = prop.get('name'))
                stored_contract._proposals.append(proposal)

            stored_contract.address = create_contract_to_blocks(stored_contract)
            # Store contract to database
            save_changes(stored_contract) 
            print("stored_contract")
            print(stored_contract)
            # Return 201 HTTP code
            return {
                'status': 'success',
                'message': 'Ballot successfully registered.',
                'contract': stored_contract.address,
                # 'proposals': json.dumps(stored_contract._proposals, cls=ProposalEncoder)
                # 'contract' : json.dumps(stored_contract, cls=ContractEncoder)
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
        if data.get('address'):
            address = web3.toChecksumAddress(data.get('address'))
            try:
                # If the Blockchain does not responding, we return 401 HTTP code  
                stored_contract = get_a_contract(address)
                ethereum_contract = get_contract_from_blocks(stored_contract)

                for user in get_all_users():
                    ethereum_contract.functions().giveRightToVote(
                        web3.toChecksumAddress(user.address)
                    ).call()
                
                return {
                    'status': 'success',
                    'message': 'The vote has been confirmed.',
                }
            except:
                return {
                    'status': 'Transaction failed',
                    'message': 'Connection with Blockchain can\'t be established '
                }, 401


     
        return {
            'status': 'success',
            'message': 'All selected voters are sign to the ballot.'
        }, 200

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