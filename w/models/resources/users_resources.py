from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from data import db_session
from models.users import User
from models.resources.users_reqparser import parser_create, parser_put


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


def abort_if_user_with_email_exist(user_email):
    session = db_session.create_session()
    if session.query(User).filter(User.email == user_email).first():
        abort(400, message=f"User with email '{user_email}' is already exist")


def abort_if_users_passwords_are_different(pass1, pass2):
    if pass1 != pass2:
        abort(409, message=f"User's password are different")


def set_password(password):
    return generate_password_hash(password)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'email', 'about'))})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        args = parser_put.parse_args()
        if 'hashed_password' in args.keys() and args['hashed_password']:
            if 'password_again' in args.keys() and args['password_again']:
                abort_if_users_passwords_are_different(args['hashed_password'], args['password_again'])
                user.set_password(args['hashed_password'])
            else:
                abort(400, message="For changing password, you must provide 'password' and 'password_again'")
        user.name = args['name'] if 'name' in args.keys() else user.name
        user.about = args['about'] if 'about' in args.keys() else user.about
        user.email = args['email'] if 'email' in args.keys() else user.email
        session.commit()
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'email', 'about'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'id': user_id})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [
            item.to_dict(only=('id', 'name', 'email', 'about')) for item in users
        ]})

    def post(self):
        args = parser_create.parse_args()
        abort_if_user_with_email_exist(args['email'])
        abort_if_users_passwords_are_different(args['hashed_password'], args['password_again'])
        session = db_session.create_session()
        user = User(
            name=args['name'],
            about=args['about'],
            email=args['email'],
            hashed_password=set_password(args['hashed_password'])
        )
        session.add(user)
        session.commit()
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'email', 'about'))})
