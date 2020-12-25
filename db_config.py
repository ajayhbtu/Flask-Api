# Importing app
from app import app

# Flask-SQLAlchemy for communicating with database
from flask_sqlalchemy import SQLAlchemy


# SQLAlchemy configuration with Mysql
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:Password@4321@localhost/excellenceDB"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemy instance
db = SQLAlchemy(app)