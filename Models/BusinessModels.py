from typing import Union, List, Dict

import datetime
from uuid import uuid4
from db import db

businessToJason = Dict[str, Union[int, str]]


class BusinessModel(db.Model):
    __tablename__ = "Businesses"
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    timestamp = db.Column(db.TIMESTAMP(), default=datetime.datetime.now())
    stores = db.relationship('StoreModel', lazy='dynamic')

    def __init__(self, _id, name: str, address: str):
        self.id = uuid4()
        self.name = name
        self.address = address

    def to_Json(self) -> businessToJason:
        return {'id': self.id, 'name': self.name, 'address': self.address}

    def insertBusiness(self) -> 'BusinessModel':
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise

    @classmethod
    def getBusiness_By_Id(cls, _id: int) -> 'BusinessModel':
        try:
            return cls.query.filter_by(id=_id).first()
        except:
            raise

    @classmethod
    def get_Business_By_Name(cls, name: str) -> 'BusinessModel':
        try:
            return cls.query.filter_by(name=name).first()
        except:
            raise

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def getAllBusinesses(cls) -> List['BusinessModel']:
        try:
            return cls.query.all()
        except:
            raise