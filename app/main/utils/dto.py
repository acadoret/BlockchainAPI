from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'email': fields.String(description='User email address'),
        'username': fields.String(description='Username'),
        'address': fields.String(description='User address'),
        'password_hash': fields.String(description='Hashed password'),
        'password': fields.String(description='password'),
    })


class ContractDto:
    api = Namespace('contract', description='Contract related operations')
    contract = api.model('contract', {
        'user_address': fields.String(description='user\'s address who create contract'),
        'name': fields.String(description='Ballot/Survey\'s name'),
        'description': fields.String(description='Description for the ballot/survey'),
        'end_date': fields.Date(description='End date of this ballot/survey'),
        # 'user': fields.Nested(UserDto.user),
        'proposals': fields.List(fields.String(description="Proposal names"))
    })

class AuthDto:
    api = Namespace('auth', description='Authentification related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

    