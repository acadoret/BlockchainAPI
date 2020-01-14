import json
import ntpath
from datetime import datetime
from os import urandom
from flask import jsonify
from app.main import db

from app.main.models.contract import Contract, ContractEncoder
from app.main.models.proposal import Proposal, ProposalEncoder
from app.main.models.user import User
from .user_service import get_all_users

from ..utils.blockchain_utils import web3
from app.main.utils.dto import ContractDto
date_format = "%d/%m/%Y"

def save_changes(data):
    print('save_contract_changes')
    print(data)
    db.session.add(data)
    print('add data')
    db.session.commit()

def get_contract_infos_from_blocks(_contract):
    ''' Get contract from blockchain '''
    _contract._proposals = list()
    try:
        eth_contract = web3.eth.contract(
            address = web3.toChecksumAddress(_contract.address),
            abi = _contract._abi
        )
        count_cadidate = eth_contract.functions.getCandidatesCount().call()
        # if len(_contract._proposals) != count_cadidate:
        for index in range(1, count_cadidate + 1):
            proposal = eth_contract.functions.candidates(index).call()
            _contract._proposals.append(Proposal(index=proposal[0], name=proposal[1], vote_count=proposal[2]))

        return _contract
    except:
        raise {
            'status': 'Transaction failed',
            'message': 'Connection with Blockchain can\'t be established. The contract cannot be fetched.'
        }
 
def get_a_contract(data):
    print('get_a_contract')
    return get_contract_infos_from_blocks(
        Contract.query.filter_by(address=data).first_or_404()
    )
    return {
        'status': 'Bad request'
    }, 403

def get_all_contracts():
    print('get_all_contracts')
    return Contract.query.all()

def get_contracts_in_progress():
    print('get_contracts_in_prograss')
    return Contract.query.filter(
        Contract.end_date > datetime.now().strftime(date_format)
    ).all_or_404()
    # .first_or_404(description = 'There is no contract in progress')

def create_contract_to_blocks(_contract):
    print('create_contract_to_blocks')
    user = User.query.filter_by(address=_contract.user_address).first() 
    try:
        # If the Blockchain does not responding, we return 401 HTTP code 
        Ballot = web3.eth.contract(abi=_contract._abi,bytecode=_contract._bytecode)
        # DECRYPT AND GET PRIVATEKEY
        private_key = web3.eth.account.decrypt(user.keystore, user.password) 
        eth_account = web3.eth.account.privateKeyToAccount(private_key)
        # Instanciate Contract
        tx = Ballot.constructor().buildTransaction({
            'from': eth_account.address,
            'nonce': web3.eth.getTransactionCount(eth_account.address)
        })
        signed = eth_account.signTransaction(tx)
        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        contract_address = tx_receipt["contractAddress"]
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=_contract._abi)
        print("Contract address : {}".format(contract_address))
        print("ACCOUNT ADDRESS : {} \n\r".format(eth_account.address))

        for proposal in _contract._proposals:
            print("GAS ESTIMATION : {} \n\r".format(contract.functions.addCandidate(proposal.name).estimateGas()))
            tx = contract.functions.addCandidate(proposal.name).buildTransaction({
                'from': eth_account.address,
                'nonce': web3.eth.getTransactionCount(eth_account.address)
            })
            signed = eth_account.signTransaction(tx)
            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
            _tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            
        # print("NUMBER OF PROPOSALS : {} \n\r".format(contract.functions.candidateCount().call()))
        return contract_address

    except:
        raise {
            'status': 'Transaction failed',
            'message': 'Connection ko with Blockchain can\'t be established. The contract cannot be created '
        }

def create_contract(data):
    print('create_contract')
    user_address = data.get('user_address')
    if user_address:
        if data.get('proposals'): 
            stored_contract = Contract(
                name = data.get('name'), 
                description = data.get('description', "Not defined"),
                end_date = datetime.strptime(data.get('end_date'), date_format),
                user_address = user_address,
                state = "in_progress"
            )
            for prop in data.get('proposals'):
                # Instanciate new Proposal object
                proposal = Proposal(name=prop)
                stored_contract._proposals.append(proposal)

            stored_contract.address = create_contract_to_blocks(stored_contract)
            # Store contract to database
            print(stored_contract.address)
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


        # return 400 HTTP code when proposals does not filled
        raise {
            'status': 'fail',
            'message': 'Proposals data doesn\'t filled correctly. Please try again.'
        }
    # return 401 HTTP code when any user does not connected 
    return {
        'status': 'fail',
        'message': 'Unauthorized user.'
    }, 401

def send_vote(data, address):
    print('send_vote')
    print("ADDRESS : {}".format(address))
    print(data)
    if not data.get('proposal_index', False) and not data.get('user_address', False):
        return json.dumps({
            'status' : 'Error',
            'message': 'You need to pass proposal_index and user_address in request.'
        }), 401
    if address:
        user = User.query.filter_by(
            address = data.get('user_address')
        ).first_or_404(description = 'User not found. Please log in.')
        db_contract = Contract.query.filter_by(
            address = address
        ).first_or_404(description = 'Ballot not found.')

        # try:
        eth_contract = web3.eth.contract(
            abi = db_contract._abi, 
            address = web3.toChecksumAddress(db_contract.address)
        )
        # DECRYPT AND GET PRIVATE KEY
        eth_account = web3.eth.account.privateKeyToAccount(
            web3.eth.account.decrypt(user.keystore, user.password) 
        )
        # print("GAS ESTIMATION : {} \n\r".format(eth_contract.functions.vote(data.get('proposal_index')).estimateGas()))
        print('OKOKOKOKOKOKOKO\n\r')
        tx = eth_contract.functions.vote(data.get('proposal_index')).buildTransaction({
            'from': eth_account.address,
            'nonce': web3.eth.getTransactionCount(eth_account.address),
            # "gasLimit":100000
        })
        signed = eth_account.signTransaction(tx)
        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        _tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        return {
            'status': 'success',
            'message': 'Your vote has successfully send'
        }, 200
        # except:
        #     pass
    return {
        'status' : 'fail',
        'message': 'You should vote for a contract.'
    }, 400

def who_win(address):
    print("Who win ?")
    print("Contract addr : {}".format(address))
    
    today = datetime.date(datetime.now())
    db_contract = Contract.query.filter_by(address=address).first_or_404()
    
    #if datetime.date(contract.end_date) != today:
    if today != today:
        return {
            'status': 'fail',
            'message': 'You could not finish the Vote yet'
        }, 400
    # try:

    db_contract = get_contract_infos_from_blocks(db_contract)
    print(db_contract)
    user = User.query.filter_by(address = db_contract.user_address).first()
    
    db_contract._proposals = sorted(
        db_contract._proposals, 
        key = lambda proposal: proposal.vote_count, 
        reverse = True
    )

    eth_contract = web3.eth.contract(
        abi = db_contract._abi, 
        address = web3.toChecksumAddress(db_contract.address)
    )

    # DECRYPT AND GET PRIVATE KEY
    eth_account = web3.eth.account.privateKeyToAccount(
        web3.eth.account.decrypt(user.keystore, user.password) 
    )
    print('db-contract')
    print(db_contract.__dict__)
    tx = eth_contract.functions.is_winner(db_contract._proposals[0].index).buildTransaction({
        'from': web3.toChecksumAddress(eth_account.address),
        'nonce': web3.eth.getTransactionCount(eth_account.address),
        'gasPrice': web3.toWei('1', 'gwei'),
        'gas':70000
    })
    signed = eth_account.signTransaction(tx)
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
    _tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    
    db_contract._proposals[0].is_winning = True
    db_contract.state = contract.state_enum.done

    return {
        'status': 'succes',
        'message': 'The ballot has been closed.',
        'winner': db_contract._proposals[0].name,
        'tx_receipt': web3.toJSON(_tx_receipt)
    }, 200
    # except:
    #      return {
    #         'status': 'Transaction failed',
    #         'message': 'Connection with Blockchain can\'t be established. The contract cannot be fetched.',
    #         'tx_receipt': Web3.toJSON(_tx_receipt)
    #     }, 400

