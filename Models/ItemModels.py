from typing import Dict, Union, List
from uuid import uuid4

from db import db

ItemJson = Dict[str, Union[int, str, float]]


class ItemModel(db.Model):
    __tablename__ = "Items"
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    produce_date = db.Column(db.DateTime(), default=True)
    expire_date = db.Column(db.DateTime(), default=True)
    price = db.Column(db.Float(precision=5))
    store_id = db.Column(db.String(), db.ForeignKey("Stores.id"))
    store = db.relationship("StoreModel")

    def __init__(
        self,
        _id,
        name: str,
        price: str,
        store_id: int,
        produce_date: str,
        expire_date: str,
    ):
        self.id = uuid4()
        self.name = name
        self.price = price
        self.store_id = store_id
        self.produce_date = produce_date
        self.expire_date = expire_date

    def to_Json(self) -> ItemJson:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "Produce Date": self.produce_date,
            "Expire Date": self.expire_date,
            "store": self.store.to_JsonNoItems(),
        }

    @classmethod
    def get_Item_By_Name(cls, name: str) -> "ItemModel":
        try:
            return cls.query.filter_by(
                name=name
            ).first()  # Replacing ItemModel with cls
        except:
            raise

    @classmethod
    def get_Item_By_Id(cls, _id: str) -> "ItemModel":
        try:
            return cls.query.filter_by(
                id=_id
            ).first()
        except:
            raise

    def insertItem(self) -> "ItemModel":
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise

    @classmethod
    def getAllItems(cls) -> List["ItemModel"]:
        try:
            return cls.query.all()
        except:
            raise

    def deleteItem(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            raise

    def updateItem(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except:
            raise
