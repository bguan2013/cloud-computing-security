from google.appengine.ext import ndb

class Event(ndb.Model):
	date = ndb.DateTimeProperty(auto_now_add=True)
	title = ndb.StringProperty()
	content = ndb.StringProperty()

	#query_all takes the event table itself and orders all by the event date in descending order 
	@classmethod
	def query_all(cls):
		return cls.query().order(-cls.date)