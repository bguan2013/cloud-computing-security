import bcrypt
from google.appengine.ext import ndb

class User(ndb.Model):

	username = ndb.StringProperty()
	password = ndb.StringProperty()

	def verify_password(plain_pwd, hashed_pwd):
		if bcrypt.checkpw(plain_pwd, hashed_pwd):
			return True
		else:
			return False

	def hash_password(plain_pwd):
		salt = bcrypt.gensalt()
		hashed_pwd = bcrypt.hashpw(plain_pwd, salt)
		return hashed_pwd

	@classmethod
	def user_exist(cls, username):
		return cls.query(User.username==username).fetch()