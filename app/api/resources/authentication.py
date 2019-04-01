from flask import g, jsonify, current_app, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from ..schemas import (
    ResetPasswordRequestSchema,
    ResetPasswordTokenSchema,
    ResetPasswordSchema,
    RegistrationSchema,
    RegistrationConfirmationSchema,
)
from ... import status, csrf, db
from ...auth.email import send_password_reset_email, send_registration_confirmation_email
from ...models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_user_password(email_or_token, password):
    if email_or_token == "":
        return False
    if password == "":
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = g.current_user is None
        return g.current_user is not None
    csrf.protect()
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@basic_auth.error_handler
def auth_error():
    return jsonify({"message": "Invalid credentials"}), status.HTTP_401_UNAUTHORIZED


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.verify_auth_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return jsonify({"message": "Token invalid"}), status.HTTP_401_UNAUTHORIZED


class TokenRequiredResource(Resource):
    method_decorators = [token_auth.login_required]


class AuthenticationResource(Resource):
    @basic_auth.login_required
    def post(self):
        if g.current_user.is_anonymous or g.token_used:
            return auth_error()
        elif not g.current_user.confirmed:
            response = {"message": "Unconfirmed account! Please confirm your account before trying to log in again.",
                        "token": g.current_user.generate_confirmation_send_again_token()}
            return response, status.HTTP_403_FORBIDDEN
        else:
            return (
                {
                    "token": g.current_user.generate_auth_token(
                        expiration=current_app.config["JWT_TOKEN_EXPIRATION_TIME"]
                    ),
                    "expiration": current_app.config["JWT_TOKEN_EXPIRATION_TIME"],
                },
                status.HTTP_200_OK
            )


class ResetPasswordResource(Resource):
    def post(self):
        csrf.protect()
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        reset_password_token_schema = ResetPasswordTokenSchema()
        errors = reset_password_token_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        response = {"message": "OK"}
        return response, status.HTTP_200_OK

    def patch(self):
        csrf.protect()
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        reset_password_schema = ResetPasswordSchema()
        errors = reset_password_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        user = User.verify_reset_password_token(request_dict["token"])
        user.password = request_dict["password"]
        user.update()
        response = {"message": "Your password has been reset"}
        return response, status.HTTP_200_OK


class ResetPasswordRequestResource(Resource):
    def post(self):
        csrf.protect()
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        reset_password_request_schema = ResetPasswordRequestSchema()
        errors = reset_password_request_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        user = User.query.filter_by(email=request_dict["email"]).first()
        if user:
            send_password_reset_email(user)
        response = {"message": "Check your email for the instructions to reset your password"}
        return response, status.HTTP_200_OK


class RegistrationResource(Resource):
    def get(self):
        csrf.protect()
        if not current_app.config["PUBLIC_REGISTRATION_ENABLED"]:
            response = {"message": "Public registration is disabled! Contact your system administrator."}
            return response, status.HTTP_403_FORBIDDEN
        response = {"message": "OK"}
        return response, status.HTTP_200_OK

    def post(self):
        csrf.protect()
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        registration_schema = RegistrationSchema()
        errors = registration_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        if not User.is_unique(id=0, email=request_dict["email"]):
            response = {"message": "A user with the same e-mail address already exists"}
            return response, status.HTTP_409_CONFLICT
        try:
            user = User(name=request_dict["name"], email=request_dict["email"], password=request_dict["password"])
            user.add(user)
            send_registration_confirmation_email(user)
            response = {
                "message": "You have been successfully registered! A confirmation email has been sent to you by email."
            }
            return response, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class RegistrationConfirmationResource(Resource):
    def put(self):
        csrf.protect()
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        registration_confirmation_schema = RegistrationConfirmationSchema()
        errors = registration_confirmation_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        user = User.verify_confirmation_send_again_token(request_dict["token"])
        if not user:
            response = {"message": "The re-confirmation link is invalid or has expired."}
            return response, status.HTTP_400_BAD_REQUEST
        send_registration_confirmation_email(user)
        response = {
            "message": "Another confirmation email has been sent to you by email. Please be more prompt this time :)"
        }
        return response, status.HTTP_200_OK

    def post(self):
        csrf.protect()
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        registration_confirmation_schema = RegistrationConfirmationSchema()
        errors = registration_confirmation_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        if not User.confirm(request_dict["token"]):
            response = {"message": "The confirmation link is invalid or has expired."}
            return response, status.HTTP_400_BAD_REQUEST
        response = {"message": "You have confirmed your account. Thanks!"}
        return response, status.HTTP_200_OK
