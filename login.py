import cgi
import json
from datetime import datetime
from datetime import timedelta
from google.appengine.ext import ndb
import webapp2
import logging
import urllib
from user import User
from event import Event
from session import Session

class Login(webapp2.RequestHandler):
	def post(self):
		try:
			json_user = json.loads(self.request.body)
			username = json_user.get('username').encode("utf-8")
			password = json_user.get('password').encode("utf-8")
			current_user = User.user_exist(username)
			if len(current_user) > 0:
				if current_user[0].password == password:
					session = Session(session_token=Session.generate_session_token(), linked_username=username, expiration_date=datetime.now()+timedelta(seconds=3600))
					session.put()
					domain = '' if 'localhost' in self.request.host else self.request.host
					self.response.set_cookie('token', session.session_token, max_age=3600, path='/', domain=domain);	
					self.response.write(json.dumps(dict(redirect_url='/index.html', status='success')))
				else:
					self.response.write(json.dumps({'status':'Wrong user password, please try again.'}))
			else:	
				self.response.write(json.dumps({'status':'User doesn\'t exist.'}))
		except Exception as e: 
			self.response.write(json.dumps({'status':'Failed to login.'}))
			logging.exception(e)

class Register(webapp2.RequestHandler):
	def post(self):
		try:
			json_user = json.loads(self.request.body)
			username = json_user.get('username').encode("utf-8")
			password = json_user.get('password').encode("utf-8")
			current_user = User.user_exist(username)
			if len(current_user) > 0:
				self.response.write(json.dumps({'status':'User already exists!'}))
			else:
				user = User(username=username, password=password)
				user.put()
				session = Session(session_token=Session.generate_session_token(), linked_username=username, expiration_date=datetime.now()+timedelta(seconds=3600))
				session.put()
				domain = '' if 'localhost' in self.request.host else self.request.host
				self.response.set_cookie('token', session.session_token, max_age=3600, path='/', domain=domain);		
				self.response.write(json.dumps(dict(redirect_url='/index.html', status='success')))
		except Exception as e: 
			self.response.write(json.dumps({'status':'Failed to register.'}))
			logging.exception(e)

class Logout(webapp2.RequestHandler):
	def post(self):
		try:
			domain = '' if 'localhost' in self.request.host else self.request.host
			session = Session.get_session(self)
			if len(session) > 0:
				session[0].key.delete()
			self.response.set_cookie('token', '', max_age=0, path='/', domain=domain);	
			self.response.write(json.dumps(dict(redirect_url='/login.html', status='success')))
		except Exception as e: 
			self.response.write(json.dumps({'status':'Failed to logout the user.'}))
			logging.exception(e)

class UserInfo(webapp2.RequestHandler):
	def post(self):
		try:
			session_info = json.loads(self.request.body)
			session_token = session_info.get('token')
			session = Session.query(Session.session_token==session_token).fetch()
			if len(session) > 0:
				self.response.write(json.dumps(dict(username=session[0].linked_username, status='success')))
			else: 
				self.response.write(json.dumps(dict(status='Failed to retreive user information.')))
		except Exception as e: 
			self.response.write(json.dumps({'status':'Failed to retreive user information.'}))
			logging.exception(e)

app = webapp2.WSGIApplication([
	('/login', Login),
	('/register', Register),
	('/logout', Logout),
	('/getuser', UserInfo)
], debug=True)