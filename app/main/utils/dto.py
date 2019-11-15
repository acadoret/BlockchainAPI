from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'email': fields.String(description='User email address'),
        'username': fields.String(description='Username'),
        'password': fields.String(description='User password'),
        'password_hash': fields.String(description='Hashed password'),
        'range': fields.Integer(description='Range for mass creating. Only used in dev.')
    })


class ContractDto:
    api = Namespace('contract', description='Contract related operations')
    contract = api.model('contract', {
        'address': fields.String(description='Ballot/Survey\'s address'),
        'name': fields.String(description='Ballot/Survey\'s name'),
        'description': fields.String(description='Description for the ballot/survey'),
        'end_date': fields.Date(description='End date of this ballot/survey')
    })

class AuthDto:
    api = Namespace('auth', description='Authentification related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

    