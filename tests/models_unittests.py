#!/usr/bin/env python3
import unittest
from sqlalchemy import *
import os
import src.models as models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/unittest.db'


class TestTokenMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            os.remove('/tmp/unittest.db')
        except:
            pass
        cls.engine = create_engine('sqlite:////tmp/unittest.db')
        cls.conn = TestTokenMethods.engine.connect()
        metadata = MetaData()
        cls.user = Table('users', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('username', String(50)),
                         Column('pw_hash', String(200), nullable=False),
                         Column('token_id', String(50))
                         )
        cls.token = Table('tokens', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('token_id', String(50)),
                     Column('is_used', Boolean)
                          )
        metadata.create_all(TestTokenMethods.engine)

    def setUp(self):
        TestTokenMethods.token.create(TestTokenMethods.engine, checkfirst=True)
        TestTokenMethods.conn.execute(TestTokenMethods.token.insert(), [
             {'token_id': '12345', 'is_used': True},
             {'token_id': '34567', 'is_used': False}
             ])

    def tearDown(self):
        TestTokenMethods.token.drop(TestTokenMethods.engine)
        pass

    def test_check_if_token_is_used(self):
        token = models.Token('12345')
        result = models.Token.check_if_token_is_used(token)
        self.assertEqual(result, True)
        token = models.Token('123456')
        result = models.Token.check_if_token_is_used(token)
        self.assertEqual(result, True)
        token = models.Token('34567')
        result = models.Token.check_if_token_is_used(token)
        self.assertEqual(result, False)

    def test_if_token_is_retrieved_correctly(self):
        token = models.Token('12345', True)
        result = models.Token.get_token(token)
        self.assertNotEqual(result, None)
        token = models.Token('12345678', True)
        result = models.Token.get_token(token)
        self.assertEqual(result, None)

    def test_if_token_is_added_correctly(self):
        token = models.Token('1234578')
        token.add()
        result = models.Token.check_if_token_is_used(token)
        self.assertEqual(result, False)

    def test_change_token_status(self):
        token = models.Token('12345', True)
        result = models.Token.get_token(token)
        result.change_token_status(False)
        token = models.Token('12345', False)
        after_update = models.Token.get_token(token)
        self.assertNotEqual(after_update, None)

if __name__ == '__main__':
    unittest.main()
