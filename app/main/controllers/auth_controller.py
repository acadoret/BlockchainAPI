from flask import request
from flask_restplus import Resource
from flask_login import login_required

from app.main.services.auth_helper import Auth
from app.main.utils.dto import AuthDto
from app.main.utils.decorators import token_required, admin_token_required
api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """ User Login Resource """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """ Logout Resource """
    @api.doc('logout a user')
    @token_required
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        print("LogoutAPI Auth_header : {}".format(auth_header))
        return Auth.logout_user(data=auth_header)