import urllib.parse as quote

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Migration
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# Security
from Security.blacklist import BLACKLIST
from Security.Security import secrete_key

# User
from Resources.User.User import (
    User,
    Users,
    UserList,
    UserLogin,
    UserLogout,
    TokenRefresh,
    DeleteUser,
    StoreUserList
)

# Items
from Resources.Store.Store import Store, Stores, StoreList, BusinessStoreList

# Store
from Resources.Item.Item import Item, Items, ItemList

# Business
from Resources.Business.Business import Business, Businesses, BusinessList

# Transaction
from Resources.Transaction.Transaction import Transaction, CreditScore, TransactionList, TransactionNumberTotal, TotalTransactionAmount
# Sparse is better than dense
app = Flask(__name__)
from db import db, mongo

app.config["MONGO_URI"] = "mongodb+srv://"+quote.quote_plus("username")+":password@cluster0.nw1wm.azure.mongodb.net/Hadi?retryWrites=true&w=majority"
mongo.init_app(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = ""
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # toggled off FlaskSQLAlchemy modification

# ""

# Migration
migrate = Migrate(app, db)
# tracker and not that of SqlAlchemy itself
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

# Required for the security
app.secret_key = secrete_key

# Flask RESTful
api = Api(app)

# Security
jwt = JWTManager(app)  # , authenticate, identity


# JWT Extended
@jwt.user_claims_loader
def add_claims_to_jwt(
    identity
):  # Remember identity is what we define when creating the access token
    if (
        identity == 1
    ):  # instead of hard-coding, we should read from a file or database to get a list of admins instead
        return {"is_admin": True}
    return {"is_admin": False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(
    error
):  # we have to keep the argument here, since it's passed in by the caller internally
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


# Resources
# Item
api.add_resource(Item, "/item")
api.add_resource(Items, "/items/<string:name>")
api.add_resource(ItemList, "/items")

# Store
api.add_resource(Store, "/store")
api.add_resource(Stores, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(BusinessStoreList, "/stores/<string:business_id>")

# User
api.add_resource(User, "/user")
api.add_resource(Users, "/users/<string:username>")
api.add_resource(UserList, "/users")
# api.add_resource(UserList, "/users/<string:username>")
api.add_resource(StoreUserList, "/users/<string:business_id>")
api.add_resource(DeleteUser, "/DeleteRecord")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

# Business
api.add_resource(Business, "/business")
api.add_resource(Businesses, "/business/<string:name>")
api.add_resource(BusinessList, "/businesses")

# Transaction
api.add_resource(Transaction, "/transaction")

api.add_resource(CreditScore, "/creditscore")

api.add_resource(TransactionList, "/getAllTransactions")

api.add_resource(TransactionNumberTotal, "/transactionnumbertotal")


api.add_resource(TotalTransactionAmount, "/totaltransactionamount")


if __name__ == "__main__":
    from db import db

    # Migration
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
    # manager.run()

    db.init_app(app)
    app.run(port=5000, debug=True)
