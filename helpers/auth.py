import bcrypt as bc
import hashlib

from helpers.pgHelper import PGHelper


class Users:
	def __init__(self, user, password):
		self.user = user
		self.active = True
		self.password = Users.hashed_password(password)

	@staticmethod
	def hashed_password(password):
		m = hashlib.sha256()
		m.update(str.encode(password))
		return m.hexdigest()

	@staticmethod
	def get_user_with_user_and_password(user, password):
		hashed = Users.hashed_password(password)

		user = PGHelper.selectOne("SELECT password FROM users WHERE userlogin='" + user + "' LIMIT 1")
		if user and bc.checkpw(hashed.encode('utf-8'), user.get('password').encode('utf-8')):
			return user
		else:
			return None

	@staticmethod
	def generate_new_password(password):
		hashed = Users.hashed_password(password)
		return bc.hashpw(hashed.encode('utf-8'), bc.gensalt(prefix=b'2a', rounds=10)).decode()

	@staticmethod
	def is_admin(ids):
		user = PGHelper.selectOne("SELECT username FROM users WHERE id=" + ids + " AND role=get_role_id('admin')")
		if user:
			return True
		return False
