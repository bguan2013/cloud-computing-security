import cgi
import json
from datetime import datetime
from google.appengine.ext import ndb
import webapp2
import logging
from event import Event

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


class Remove(webapp2.RequestHandler): 
	def delete(self, id):
		event_id = 'Does not exist'
		try:
			path_array = self.request.path.split('/')
			logging.info('path array: ' + repr(path_array))
			if len(path_array) > 1:
				event_id = path_array[len(path_array)-1]		
				#Event.query(Event.Key.id() == event_id).fetch().delete()
				ndb.Key(urlsafe=event_id).delete()
				self.response.write(json.dumps(dict(id=repr(event_id), status='success')))
		except Exception as e:
			self.response.write(json.dumps(dict(id=repr(event_id), status='failed to delete event')))
			logging.exception(e)


class SubmitForm(webapp2.RequestHandler):
	def post(self):
		try:
			json_event = json.loads(self.request.body)
			event_title = json_event.get('title')
			event_content = json_event.get('content')  
			event_date = datetime.strptime(json_event.get('date'), '%Y-%m-%d')
			event = Event(title=event_title, content=event_content, date=event_date)
			event.put()
			self.response.write(json.dumps(dict(id=repr(event.key.urlsafe()), status='success')))
		except Exception as e: 
			self.response.write(json.dumps(dict(id=repr(event.key.urlsafe()), status='failed to save event')))
			logging.exception(e)

class AllEvents(webapp2.RequestHandler):
	def date_handler(obj):
	    if hasattr(obj, 'isoformat'):
	        return obj.isoformat()
	def get(self):
		all_events = [dict(e.to_dict(), **dict(id=repr(e.key.urlsafe()))) for e in Event.query_all().fetch()]
		all_events_json = json.dumps(all_events, cls=Encoder, indent=4)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(all_events_json)

app = webapp2.WSGIApplication([
	('/events', AllEvents),
	('/event', SubmitForm),
	('/event/(.*)', Remove)
], debug=True)


