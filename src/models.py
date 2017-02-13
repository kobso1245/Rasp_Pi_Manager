#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from . import exceptions
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/unittest.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    pw_hash = db.Column(db.String(200), unique=True)
    token_id = db.Column(db.String(50), unique=True)

    @staticmethod
    def check_if_user_exists(user_instance):
        username = user_instance.username
        all_registered_users = User.query.all()
        all_registered_usernames = [_.name for _ in all_registered_users]
        return True if username in all_registered_usernames else False

    def __init__(self, name=None, email=None, pw_hash=None):
        self.username = name
        self.pw_hash = pw_hash

    def __repr__(self):
        return '<User %r>' % (self.username)

    def register(self, username, pw_hash, token_id):
        pass


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(50), unique=True)
    is_used = db.Column(db.Boolean, default=False)

    @staticmethod
    def create_token():
        already_taken = [_.token_id for _ in Token.get_all_tokens()]
        new_token_id = ''
        while True:
            token = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits)
                            for _ in range(30))
            if token not in already_taken:
                new_token_id = token
                break

        # create new token for auth
        token = Token(gen_id=new_token_id, is_used=False)
        token.add()
        return token

    @staticmethod
    def get_all_tokens():
        return Token.query.all()

    @staticmethod
    def check_if_token_is_used(token_instance):
        token_id = token_instance.token_id
        token = Token.query.filter(and_(Token.is_used == 0,
                                        Token.token_id == token_id)).all()
        return False if token else True

    @staticmethod
    def get_token(token_instance):
        token_id = token_instance.token_id
        token_used = 1 if token_instance.is_used else 0
        token = Token.query.filter(and_(Token.is_used == token_used,
                                        Token.token_id == token_id)).all()
        return token[0] if token != [] else None

    def __init__(self, gen_id=None, is_used=False):
        self.token_id = gen_id
        self.is_used = is_used

    def add(self):
        db.session.add(self)
        db.session.commit()

    def change_token_status(self, new_status):
        token = Token.get_token(self)
        if token:
            token.is_used = new_status
            db.session.commit()
