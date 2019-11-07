import uuid

from datetime import datetime
from os import urandom

from ..utils.blockchain_utils import web3
from eth_account import Account

from app.main import db
from app.main.models.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        entropy = urandom(64)
        eth_acc = web3.geth.personal.newAccount(str(entropy))
        print(eth_acc)
        # eth_account = Account.create(entropy)
        
        # with open('~/.ethereum/keystore/UTC--...--5ce9454909639D2D17A3F753ce7d93fa0b9aB12E') as keyfile:
        #     encrypted_key = keyfile.read()
        #     private_key = web3.eth.account.decrypt(encrypted_key, entropy)
        
        
        # print("ETH ACC TEST : OBJT = %s" % eth_acc)
        # print("ETH ACC TEST : ADDR = %s" % eth_acc.address)
        # # print("ETH ACC TEST : PUBKEY  = %s" % eth_acc.key)
        # # print("ETH ACC TEST : PRIKEY  = %s" % eth_acc.privateKey)
        # print(eth_acc.key == eth_acc.privateKey)
        new_user = User(
            address=eth_acc.address,
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    # print(User.query.all())
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()