import unittest
import users
from sqlalchemy.sql import text
from test_util import init_test, MockupRequest
from werkzeug.security import check_password_hash, generate_password_hash

init_sql = """
INSERT INTO users (username, password) VALUES (:username, :password);
"""

class UsersTest(unittest.TestCase):
	def setUp(self):
		self.app, self.db = init_test()	

		with self.app.app_context():
			test_users = {
				"username": "user1",
				"password": generate_password_hash("password1")
			}

			self.db.session.execute(text(init_sql), test_users)
			self.db.session.commit()

	def test_register_success(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertTrue(users.register(self.db, "new_user", "new_user_password"))

	def test_register_taken_username(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertFalse(users.register(self.db, "user1", "password1"))
			self.assertFalse(users.register(self.db, "user1", "new_password"))

	def test_login_success(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertTrue(users.login(self.db, "user1", "password1"))

	def test_login_with_bad_user(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertFalse(users.login(self.db, "user123456", "password"))

	def test_login_with_wrong_password(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertFalse(users.login(self.db, "user1", "wrong password"))
