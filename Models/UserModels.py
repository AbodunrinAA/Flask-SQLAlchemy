from typing import Union, List, Dict

import datetime
from uuid import uuid4

from db import db

userToJason = Dict[str, Union[int, str]]


class UserModel(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.String(), primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String())
    role = db.Column(db.String(), default='User')
    timestamp = db.Column(db.TIMESTAMP(), default=datetime.datetime.now())
    store_id = db.Column(db.String(), db.ForeignKey("Stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, _id, firstname: str, lastname: str, username: str, password: str, store_id: str, role: str = 'User'):
        self.id = uuid4()
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.role = role
        self.store_id = store_id

    def to_Json(self) -> userToJason:
        return {'id': self.id, 'firstname': self.firstname, 'lastname': self.lastname, 'username': self.username,
                'store_id': self.store_id, 'role': self.role}

    def insertUser(self) -> 'UserModel':
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise

    @classmethod
    def getUser_By_Username(cls, username: str) -> 'UserModel':
        try:
            return cls.query.filter_by(username=username).first()
        except:
            raise

    @classmethod
    def getUser_By_Id(cls, _id: str) -> 'UserModel':
        try:
            return cls.query.filter_by(id=_id).first()
        except:
            raise

    @classmethod
    def getUser_By_business_id(cls, store_id: str) -> List['UserModel']:
        try:
            return cls.query.filter_by(store_id=store_id)
        except:
            raise

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def getAllUsers(cls) -> List['UserModel']:
        try:
            return cls.query.all()
        except:
            raise
