from http import HTTPStatus
from settings import app, jwt
from controller.auth import auth
from controller.user import user
from util.advice import ErrorHandler
from flask_jwt_extended import exceptions
from util.helpers import json_response

app.register_blueprint(auth, url_prefix='/api/v1/auth')
app.register_blueprint(user, url_prefix='/api/v1/user')


@app.route('/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def index():
    return {"Hello": "World"}


@app.errorhandler(exceptions.NoAuthorizationError)
@app.errorhandler(exceptions.CSRFError)
@app.errorhandler(exceptions.JWTExtendedException)
@app.errorhandler(exceptions.UserLookupError)
@app.errorhandler(exceptions.JWTDecodeError)
@app.errorhandler(exceptions.FreshTokenRequired)
@app.errorhandler(exceptions.WrongTokenError)
@app.errorhandler(exceptions.UserClaimsVerificationError)
@app.errorhandler(exceptions.RevokedTokenError)
@app.errorhandler(exceptions.InvalidHeaderError)
@app.errorhandler(exceptions.InvalidQueryParamError)
@jwt.invalid_token_loader
@jwt.user_lookup_error_loader
@jwt.unauthorized_loader
@jwt.additional_claims_loader
@jwt.additional_headers_loader
@jwt.encode_key_loader
@jwt.expired_token_loader
@jwt.revoked_token_loader
@jwt.needs_fresh_token_loader
def handle_auth_error(e):
    return json_response(data=str(e), code=HTTPStatus.UNAUTHORIZED.real)


@app.errorhandler(Exception)
def handle_exceptions(error):
    return ErrorHandler(error).response


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
