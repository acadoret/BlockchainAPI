import json
import requests
import ntpath
from datetime import datetime

from app.main import db
from app.main.models.user import User, UserEncoder
from app.main.utils.blockchain_utils import web3
from app.main.utils.dto import UserDto


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.address)
        return {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode(),
            'user' : json.dumps(user, cls=UserEncoder)
        }, 201

    except Exception as e:
        return {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }, 401

def path_leaf(path):
    """
    This delete the left part of given path
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def mass_creating(_range):
    _data= {}
    for _index in range(0,_range):
        _data['password'] = "dummy"
        _data['username'] = "dummy_{}".format(_index)
        _data['email'] = "dummy_{}".format(_index)
        _data['index'] = _index
        save_new_user(data=_data)
    return {
        'status': 'success',
        'message': '{} Users are successfully registered.'.format(_range),
    }, 201 

def send_ether(user):
    print('send_ether')
    print("ETH ON MAIN ACCOUNT : {}".format(web3.fromWei(web3.eth.getBalance('0x14f021B82a5752C7f0bBb1d5eF5f7bD4b22e4070'), 'ether')))
    main_account = User.query.filter_by(address='0x14f021B82a5752C7f0bBb1d5eF5f7bD4b22e4070').first_or_404(description="Main user not found")
    signed_txn = web3.eth.account.signTransaction(dict(
        nonce = web3.eth.getTransactionCount('0x14f021B82a5752C7f0bBb1d5eF5f7bD4b22e4070'),
        gasPrice = web3.eth.gasPrice, 
        gas = 100000,
        to = user.address,
        value = web3.toWei(0.5,'ether')
    ), web3.eth.account.decrypt(main_account.keystore, main_account.password))

    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    _tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("ETH ON CREATED ACCOUNT : {}".format(web3.fromWei(web3.eth.getBalance(user.address), 'ether')))
    return _tx_receipt 

def save_new_user(data):
    """
    Saver in DB : This create a User object in SQLiteDB with given parameters  
    """
    user = User.query.filter_by(email=data['email']).first()
    # eth_acc = personal.newAccount("<YOUR_PASSWORD>")
        
    if not user:
        account = web3.eth.account.create()
        new_user = User(
            address=account.address,
            path_to_key="",
            password=data.get('password'),
            email=data.get('email'),
            username=data.get('username'),
            registered_on=datetime.utcnow()
        )
        new_user.keystore = account.encrypt(new_user.password)
        
        save_changes(new_user)
        # curl -X GET https://faucet.ropsten.be/donate/0x14f021B82a5752C7f0bBb1d5eF5f7bD4b22e4070
        r = requests.get("https://faucet.ropsten.be/donate/{}".format(new_user.address))
        print("request")
        print(r.content)
        print("ETH ON CREATED ACCOUNT : {}".format(web3.fromWei(web3.eth.getBalance(new_user.address), 'ether')))
        if r.status_code == 403:
            tx = send_ether(new_user)
            print("tx send ether")
            print(tx)

        return generate_token(new_user)
        
    return {
        'status': 'fail',
        'message': 'User already exists. Please Log in.',
    }, 409


def get_all_users():
    print('get_all_users')
    return User.query.all()

def get_a_user(email):
    print('get_a_user')
    return User.query.filter_by(email=email).first_or_404(
        description='There is no data with {}'.format(email)
    )

def is_connected(data):
    print('is_connected')
    user = User.query.filter_by(email=data.get('email')).first()
    # Check if the given password match with the stored password
    if user and user.check_password(data['password']):
        return {
            'status' : 'success',
            'message' : 'Successfully connected.',
            'user' : json.dumps(user, cls=UserEncoder)
        }, 201
        
    return {
        'status': 'fail',
        'message': 'Incorrect login credentials. Please try again or create an account.'
    }, 409

def save_changes(data):
    print('save_changes')
    db.session.add(data)
    db.session.commit()
