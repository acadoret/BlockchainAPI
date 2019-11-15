from flask import request
from flask_restplus import Resource

from ..utils.dto import UserDto
from ..services.user_service import save_new_user, get_all_users, get_a_user, is_connected

api = UserDto.api
_user = UserDto.user


@api.route('/', methods=['GET','POST'])
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        print('get_user')
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        print('post_user')
        # TODO: Faire la partie création wallet 
        # ETH et placer l'@ETH dans data 
        data = request.json
        return save_new_user(data=data)


@api.route('/<email>', methods=['GET'])
@api.param('email', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, data):
        """get a user given its identifier"""
        print('get_a_user')
        user = get_a_user(data['email'])
        if not user:
            api.abort(404)
        else:
            return user

@api.route('/auth', methods=['POST'])
@api.param('email', 'The User identifier')
@api.param('password', 'His password')
@api.response(404, 'User not found.')
class AuthUser(Resource):
    @api.response(201, 'User successfully logged.')
    @api.doc('authentificate a user')
    @api.expect(_user, validate=True)
    def post(self):
        """Authentificate a user"""
        print('is_connected')
        data = request.json
        return is_connected(data)
