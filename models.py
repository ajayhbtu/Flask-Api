# importing db
from db_config import db


# User Model
class UserModel(db.Model):
    __tablename__ = "Users"
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


# Address Model
class AddressModel(db.Model):
    __tablename__ = "Addresses"
    addrId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street = db.Column(db.String(100))
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    userId = db.Column(
        db.Integer,
        db.ForeignKey("Users.userid", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
