import json
import ntpath
from datetime import datetime
from os import urandom

from app.main import db
from app.main.models.user import User
from app.main.models.contract import Contract, ContractEncoder
from app.main.models.proposal import Proposal

from ..utils.blockchain_utils import web3


def create_contract(data):
    print('create_contract')
    user = data['user']
    if user:
        eth = web3.eth
        tx_receipt, contract = None
        # Abi contains a single .sol contract compiled in JSON
        abi = json.loads('[{"constant":false,"inputs":[{"internalType":"uint256","name":"proposal","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"proposals","outputs":[{"internalType":"address","name":"id","type":"address"},{"internalType":"bytes32","name":"name","type":"bytes32"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"delegate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"winningProposal","outputs":[{"internalType":"uint256","name":"winningProposal_","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"voter","type":"address"}],"name":"giveRightToVote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"chairPerson","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"winnerName","outputs":[{"internalType":"bytes32","name":"winnerName_","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"proposalNames","type":"bytes32[]"},{"internalType":"address[]","name":"proposalAddrs","type":"address[]"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
        # Bytecode contains the bytecode of a complied contract 
        bytecode = '608060405234801561001057600080fd5b506040516108843803806108848339818101604052604081101561003357600080fd5b810190808051604051939291908464010000000082111561005357600080fd5b90830190602082018581111561006857600080fd5b825186602082028301116401000000008211171561008557600080fd5b82525081516020918201928201910280838360005b838110156100b257818101518382015260200161009a565b50505050905001604052602001805160405193929190846401000000008211156100db57600080fd5b9083019060208201858111156100f057600080fd5b825186602082028301116401000000008211171561010d57600080fd5b82525081516020918201928201910280838360005b8381101561013a578181015183820152602001610122565b50505050919091016040908152600080546001600160a01b03191633178082556001600160a01b031681526001602081905291812082019190915593505050505b8251811115610223576002604051806060016040528084848151811061019d57fe5b60200260200101516001600160a01b031681526020018584815181106101bf57fe5b6020908102919091018101518252600091810182905283546001808201865594835291819020835160039093020180546001600160a01b0319166001600160a01b03909316929092178255820151818401556040909101516002909101550161017b565b50505061064f806102356000396000f3fe608060405234801561001057600080fd5b506004361061007d5760003560e01c8063609ff1bd1161005b578063609ff1bd1461010c5780639e7b8d6114610126578063d4d4b5ac1461014c578063e2ba53f0146101705761007d565b80630121b93f14610082578063013cf08b146100a15780635c19a95c146100e6575b600080fd5b61009f6004803603602081101561009857600080fd5b5035610178565b005b6100be600480360360208110156100b757600080fd5b503561021c565b604080516001600160a01b039094168452602084019290925282820152519081900360600190f35b61009f600480360360208110156100fc57600080fd5b50356001600160a01b0316610256565b610114610450565b60408051918252519081900360200190f35b61009f6004803603602081101561013c57600080fd5b50356001600160a01b03166104b7565b6101546105b7565b604080516001600160a01b039092168252519081900360200190f35b6101146105c6565b336000908152600160205260409020600281015460ff16156101d2576040805162461bcd60e51b815260206004820152600e60248201526d20b63932b0b23c903b37ba32b21760911b604482015290519081900360640190fd5b6002808201805460ff19166001908117909155600383018490558201548154909190849081106101fe57fe5b60009182526020909120600260039092020101805490910190555050565b6002818154811061022957fe5b60009182526020909120600390910201805460018201546002909201546001600160a01b03909116925083565b336000908152600160205260409020600281015460ff16156102b4576040805162461bcd60e51b81526020600482015260126024820152712cb7ba9030b63932b0b23c903b37ba32b21760711b604482015290519081900360640190fd5b6001600160a01b038216331415610312576040805162461bcd60e51b815260206004820152601e60248201527f53656c662d64656c65676174696f6e20697320646973616c6c6f7765642e0000604482015290519081900360640190fd5b6001600160a01b03828116600090815260016020526040902060020154610100900416156103ba576001600160a01b03918216600090815260016020526040902060020154610100900490911690338214156103b5576040805162461bcd60e51b815260206004820152601960248201527f466f756e64206c6f6f7020696e2064656c65676174696f6e2e00000000000000604482015290519081900360640190fd5b610312565b600280820180546001600160a01b0385166101008102610100600160a81b031960ff19909316600190811793909316179092556000918252602052604090209081015460ff161561043a578160010154600282600301548154811061041b57fe5b600091825260209091206002600390920201018054909101905561044b565b600180830154908201805490910190555b505050565b600080805b6002548110156104b257816002828154811061046d57fe5b90600052602060002090600302016002015411156104aa576002818154811061049257fe5b90600052602060002090600302016002015491508092505b600101610455565b505090565b6000546001600160a01b031633146105005760405162461bcd60e51b81526004018080602001828103825260278152602001806105f46027913960400191505060405180910390fd5b6001600160a01b03811660009081526001602052604090206002015460ff1615610571576040805162461bcd60e51b815260206004820152601760248201527f54686520766f74657220616c726561647920766f746564000000000000000000604482015290519081900360640190fd5b6001600160a01b038116600090815260016020819052604090912001541561059857600080fd5b6001600160a01b03166000908152600160208190526040909120810155565b6000546001600160a01b031681565b600060026105d2610450565b815481106105dc57fe5b90600052602060002090600302016001015490509056fe4f6e6c79206368616972506572736f6e2063616e206769766520726967687420746f20766f7465a265627a7a723158205f0638fde35f78a5a790ce6459178b4dcf8aaeb09d7f325aaa2f8e2b70b9c9a764736f6c634300050b0032'
        # Create a new Ballot.sol contract  
        ballot = eth.contract(abi=abi,bytecode=bytecode)   
        proposalNames, proposalAddrs = list()   
        
        if data['proposals']: 
            for prop in data['proposals']:
                # Instanciate new Proposal object
                proposal = Proposal(_name=bytes(prop['name'],'utf-8'), _address=web3.toChecksumAddress(prop['address']))
                proposalNames.append(proposal.name)
                proposalAddrs.append(proposal.address)
            try:
                # If the Blockchain does not responding, we return 401 HTTP code  
                tx_hash = ballot.constructor(proposalNames,proposalAddrs).transact()
                tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
                contract = web3.eth.contract(
                    address = tx_receipt.contractAddress,
                    abi = abi
                )
            except:
                return {
                    'status': 'Transaction failed',
                    'message': 'Connection with Blockchain can\'t be established '
                }, 401
            # Store the new ballot to database
            new_ballot = save_new_contract(data) 
            # Return 201 HTTP code
            return {
                'status': 'success',
                'message': 'Ballot successfully registered.',
                'contract' : json.dumps(new_ballot, cls=ContractEncoder)
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

def get_all_contracts():
    print('get_all_contracts')
    return Contract.query.all()

def get_a_contract(data):
    print('get_a_contract')
    if data['address']:
        return Contract.query.filter_by(address=data['address']).first()
    else:
        return Contract.query.filter_by(address=data['name'])

def save_new_contract(data):
    print('save_new_contract')
    # Instanciate new contract
    new_contract = Contract(
        address = data['contractAddress'], 
        name = data['name'], 
        description = data['descripiton'],
        end_date = datetime.strptime(data['end_date'], "%d/%m/%Y"),
        user_id = data['user']['address']
    )
    # Store contract to database
    save_changes(new_contract)
    return new_contract

def save_changes(data):
    print('save_changes')
    db.session.add(data)
    db.session.commit()
