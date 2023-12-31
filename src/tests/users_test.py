import unittest
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from test_util import init_test
import users

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
			self.assertGreater(users.user_id(), 0)

	def test_register_taken_username(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertFalse(users.register(self.db, "user1", "password1"))
			self.assertFalse(users.register(self.db, "user1", "new_password"))
			self.assertEqual(users.user_id(), 0)

	def test_login_success(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertTrue(users.login(self.db, "user1", "password1"))
			self.assertGreater(users.user_id(), 0)

	def test_login_with_bad_user(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertFalse(users.login(self.db, "user123456", "password"))
			self.assertEqual(users.user_id(), 0)

	def test_login_with_wrong_password(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertFalse(users.login(self.db, "user1", "wrong password"))
			self.assertEqual(users.user_id(), 0)

	def test_logout_after_login(self):
		with self.app.app_context(), self.app.test_request_context():
			self.assertTrue(users.login(self.db, "user1", "password1"))
			users.logout()
			self.assertEqual(users.user_id(), 0)
