from flask import Flask

# Flask-RESTful for creating api
from flask_restful import Api, Resource, reqparse, abort

# App Instance
app = Flask(__name__)

# importing db
from db_config import db


# importing Models
from models import UserModel, AddressModel

# passlib for saving the hashed password into the database
from passlib.hash import pbkdf2_sha256 as sha256


# Api instance
api = Api(app)


# Setting form data parser for registration and login
user_args = reqparse.RequestParser()
user_args.add_argument(
    "username", type=str, help="username is mendetory", required=True
)
user_args.add_argument(
    "password", type=str, help="password is mendetory", required=True
)


# Setting form data parser for adding Addresses
address_args = reqparse.RequestParser()
address_args.add_argument("street", type=str)
address_args.add_argument("state", type=str, help="state is mendetory", required=True)
address_args.add_argument(
    "country", type=str, help="country is mendetory", required=True
)
address_args.add_argument(
    "pincode", type=str, help="pincode is mendetory", required=True
)
address_args.add_argument("phone", type=str, help="phone is mendetory", required=True)
address_args.add_argument("userId", type=int, help="userId is mendetory", required=True)


# Setting form data parser for updating Addresses
update_address_args = reqparse.RequestParser()
update_address_args.add_argument("street", type=str)
update_address_args.add_argument("state", type=str)
update_address_args.add_argument("country", type=str)
update_address_args.add_argument("pincode", type=str)
update_address_args.add_argument("phone", type=str)
update_address_args.add_argument(
    "userId", type=int, help="userId is mendetory", required=True
)


# Resource for user registration/save
class UserRegistration(Resource):
    def post(self):
        args = user_args.parse_args()
        result = UserModel.query.filter_by(username=args["username"]).first()
        if result:
            abort(409, message="User already exists")

        user = UserModel(
            username=args["username"], password=sha256.hash(args["password"])
        )
        db.session.add(user)
        db.session.commit()
        return {"message": f"User {args['username']} is Successfully Registered!"}, 201


# Resource for user login
class UserLogin(Resource):
    def post(self):
        args = user_args.parse_args()
        result = UserModel.query.filter_by(username=args["username"]).first()
        if not result:
            abort(404, message=f"User {args['username']} doesn't exist!")

        if sha256.verify(args["password"], result.password):
            return {"message": f"Logged in as {args['username']}!"}, 200

        else:
            return {"message": "Wrong Credentials!"}, 401


# Resource for adding and updating addresses
class UserAddress(Resource):
    def post(self, addrId):
        args = address_args.parse_args()
        result = UserModel.query.filter_by(userid=args["userId"]).first()
        if not result:
            abort(
                404,
                message=f"Any existing Users does not have userid {args['userId']} i.e Please provide a valid User id to associate this address!",
            )

        address_result = AddressModel.query.filter_by(addrId=addrId).all()

        if address_result:
            for addr in address_result:
                if args["userId"] == addr.userId:
                    abort(
                        409,
                        message=f"This Address with address id {addrId} is already associated with User {result.username} with user id {addr.userId}!",
                    )

        address = AddressModel(
            addrId=addrId,
            street=args["street"],
            state=args["state"],
            country=args["country"],
            pincode=args["pincode"],
            phone=args["phone"],
            userId=args["userId"],
        )
        db.session.add(address)
        db.session.commit()
        return {"message": f"{result.username} has successfully added an address!"}, 201

    def patch(self, addrId):
        args = update_address_args.parse_args()
        user_result = UserModel.query.filter_by(userid=args["userId"]).first()

        if not user_result:
            abort(
                404,
                message=f"Any existing Users does not have userid {args['userId']} i.e Please provide a valid User id to associate this address!",
            )

        address_result = AddressModel.query.filter_by(addrId=addrId).all()

        if not address_result:
            abort(
                404, message=f"Please provide a valid Address id to update the address!"
            )

        for addr in address_result:
            if args["userId"] == addr.userId:
                if args["street"]:
                    addr.street = args["street"]
                if args["state"]:
                    addr.state = args["state"]
                if args["country"]:
                    addr.country = args["country"]
                if args["pincode"]:
                    addr.pincode = args["pincode"]
                if args["phone"]:
                    addr.phone = args["phone"]
                break
        db.session.commit()
        return {
            "message": f"Address Id {addrId} of user id {user_result.userid} has been successfully updated!"
        }, 200


# api end ponits
api.add_resource(UserRegistration, "/registration")
api.add_resource(UserLogin, "/login")
api.add_resource(UserAddress, "/address/<int:addrId>")
