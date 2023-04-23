from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from models.news import News
from models.users import User
from models.resources.news_reqparser import parser_create, parser_get, parser_put


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('id', 'title', 'content', 'created_date', 'is_private',
                  'user.id', 'user.name', 'user.email'))})

    def put(self, news_id):
        abort_if_news_not_found(news_id)
        args = parser_put.parse_args()
        abort_if_user_not_found(args['user_id'] if 'user_id' in args.keys() else -1)
        session = db_session.create_session()
        if 'user_id' in args.keys() and args['user_id']:
            user = session.query(User).get(args['user_id'])
            if user:
                news = session.query(News).filter(News.id == news_id, News.user == user).first()
                if news:
                    news.title = args['title'] if 'title' in args.keys() else news.title
                    news.content = args['content'] if 'content' in args.keys() else news.content
                    news.is_private = args['is_private'] if 'is_private' in args.keys() else news.is_private
                    session.commit()
                    return jsonify({'news': news.to_dict(
                        only=('id', 'title', 'content', 'created_date', 'is_private',
                              'user.id', 'user.name', 'user.email'))})
        return abort(403, message=f"User has no permissions to edit news '{news_id}'")

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        args = parser_get.parse_args()
        abort_if_user_not_found(args['user_id'] if 'user_id' in args.keys() else -1)
        is_authenticated = args['is_authenticated'] if 'is_authenticated' in args.keys() else False
        user_id = args['user_id'] if 'user_id' in args.keys() else -1
        session = db_session.create_session()
        if is_authenticated:
            if user_id:
                user = session.query(User).get(user_id)
                if user:
                    news = session.query(News).filter(News.id == news_id, News.user == user).first()
                    if news:
                        session.delete(news)
                        session.commit()
                        return jsonify({'id': news_id})
        return abort(403, message=f"User has no permissions to delete news '{news_id}'")


class NewsListResource(Resource):
    def get(self):
        args = parser_get.parse_args()
        is_authenticated = args['is_authenticated'] if 'is_authenticated' in args.keys() else False
        user_id = args['user_id'] if 'user_id' in args.keys() else -1
        session = db_session.create_session()
        news = session.query(News).filter(News.is_private != True)
        if is_authenticated:
            if user_id:
                user = session.query(User).get(user_id)
                if user:
                    news = session.query(News).filter((News.user == user) | (News.is_private != True))
        return jsonify({'news': [item.to_dict(
            only=('id', 'title', 'content', 'created_date',
                  'user.id', 'user.name', 'user.email')) for item in news]})

    def post(self):
        args = parser_create.parse_args()
        abort_if_user_not_found(args['user_id'] if 'user_id' in args.keys() else -1)
        session = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'news': news.to_dict(
            only=('id', 'title', 'content', 'created_date', 'is_private',
                  'user.id', 'user.name', 'user.email'))})
