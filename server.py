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
	def post(self):
		event_title = self.request.get('event-id')
		remove_event = Event.query().get()
		remove_event.delete()

class SubmitForm(webapp2.RequestHandler):
	def post(self):
		try:
			event_title = self.request.get('title')
			event_content = self.request.get('content')  
			event_date = datetime.strptime(self.request.get('date'), '%Y-%m-%d')
			event = Event(title=event_title, content=event_content, date=event_date)
			event.put()
			self.response.set_cookie('submit_status', 'Success')
			self.response.set_cookie('event_id', repr(event.key.id()))
		except Exception as e: 
			self.response.set_cookie('submit_status', 'Failed to save event')
			logging.exception(e)
		self.redirect('/index.html')


class AllEvents(webapp2.RequestHandler):
	def date_handler(obj):
	    if hasattr(obj, 'isoformat'):
	        return obj.isoformat()
	def get(self):
		all_events = [e.to_dict() for e in Event.query_all().fetch()]
		all_events_json = json.dumps(all_events, cls=Encoder, indent=4)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(all_events_json)

app = webapp2.WSGIApplication([
	('/event', SubmitForm),
	('/events', AllEvents),
	('/event/*', Remove)
], debug=True)


