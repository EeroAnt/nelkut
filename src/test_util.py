import subprocess
import platform
from os import getenv
from flask import Flask
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy

class MockupRequest:
	def __init__(self, form):
		self.form = form

__test_app = Flask(__name__)
__test_app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE")
__test_db = SQLAlchemy()

with __test_app.app_context():
	__test_db.init_app(__test_app)
	__test_app.secret_key = getenv("SECRET_KEY")

def init_test(init_sql=None):
	if platform.system() == "Windows":
		subprocess.call("bash reset_test_db.bash")
	else:
		subprocess.call("./reset_test_db.bash")

	if init_sql:
		with __test_app.app_context():
			__test_db.session.execute(text(init_sql))
			__test_db.session.commit()

	return __test_app, __test_db
