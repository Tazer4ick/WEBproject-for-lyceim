from flask_restful import reqparse

parser_create = reqparse.RequestParser()
parser_create.add_argument('title', required=True)
parser_create.add_argument('content', required=True)
parser_create.add_argument('is_private', required=True, type=bool)
parser_create.add_argument('user_id', required=True, type=int)

parser_get = reqparse.RequestParser()
parser_get.add_argument('is_authenticated', location='args', type=bool)
parser_get.add_argument('user_id', location='args')

parser_put = reqparse.RequestParser()
parser_put.add_argument('title')
parser_put.add_argument('content')
parser_put.add_argument('is_private', type=bool)
parser_put.add_argument('user_id', required=True, type=int)
