from typing import Dict, List, Union
from uuid import uuid4

from Models.ItemModels import ItemJson
from db import db

StoreJsonNoItem = Dict[str, Union[str, int]]

StoreJsonWithItems = Dict[str, Union[str, int, List[ItemJson]]]


class StoreModel(db.Model):
    __tablename__ = 'Stores'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(50))
    number = db.Column(db.String(50))
    email = db.Column(db.String(50))

    # business
    business_id = db.Column(db.String(), db.ForeignKey("Businesses.id"))
    business = db.relationship("BusinessModel")

    # item
    items = db.relationship('ItemModel', lazy='dynamic')

    # user
    users = db.relationship('UserModel', lazy='dynamic')

    def __init__(self, _id, name: str, address: str, number: str, email: str, business_id):
        self.id = uuid4()
        self.name = name
        self.address = address,
        self.number = number,
        self.email = email,
        self.business_id = business_id

    def to_JsonNoItems(self) -> StoreJsonNoItem:
        return {'id': self.id, 'name': self.name,
                'address': self.address, 'number': self.number, 'email': self.email, 'business_id': self.business_id}

    def to_Json(self) -> StoreJsonWithItems:
        return {'id': self.id, 'name': self.name,
                'address': self.address, 'number': self.number, 'email': self.email, 'business_id': self.business_id,
                'items': [item.to_Json() for item in self.items.all()]}

    @classmethod
    def get_Store_By_Name(cls, name: str) -> 'StoreModel':
        try:
            return cls.query.filter_by(name=name).first()  # Replacing StoreModel with cls
        except:
            raise

    @classmethod
    def get_Store_By_Id(cls, id: str) -> 'StoreModel':
        try:
            return cls.query.filter_by(id=id).first()  # Replacing StoreModel with cls
        except:
            raise

    @classmethod
    def get_Stores_By_Business_Id(cls, business_id: str) -> List['StoreModel']:
        try:
            return cls.query.filter_by(business_id=business_id)
        except:
            raise

    def insertStore(self) -> 'StoreModel':
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise

    @classmethod
    def getAllStores(cls) -> List['StoreModel']:
        try:
            return cls.query.all()
        except:
            raise

    def deleteStore(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            raise

    def updateStore(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except:
            raise
