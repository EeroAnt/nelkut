
from flask_sqlalchemy import SQLAlchemy
from os import getenv
db = SQLAlchemy()

engine = db.create_engine(getenv("DATABASE"))


def query(sql, params=None):
	with engine.connect().execution_options(
		isolation_level="AUTOCOMMIT"
	) as connection:
		with connection.begin():
			connection.execute(sql, params or ())