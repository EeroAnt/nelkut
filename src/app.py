from flask import Flask
from db import db
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE")
app.secret_key = getenv("SECRET_KEY")
db.init_app(app)

import routes
