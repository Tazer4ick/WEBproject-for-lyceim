from flask_restful import reqparse

parser_create = reqparse.RequestParser()
parser_create.add_argument('name', required=True)
parser_create.add_argument('about', required=True)
parser_create.add_argument('email', required=True)
parser_create.add_argument('hashed_password', required=True)
parser_create.add_argument('password_again', required=True)

parser_put = reqparse.RequestParser()
parser_put.add_argument('name')
parser_put.add_argument('about')
parser_put.add_argument('email')
parser_put.add_argument('hashed_password')
parser_put.add_argument('password_again')
