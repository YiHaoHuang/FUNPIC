import os
import urllib
import time
import json
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from stream import *

import jinja2
import webapp2

DEFAULT_STREAM_NAME = 'default_stream'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class GeoView(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('template/geo_page.html')
        stream_name = self.request.get('stream_name')
        stream_query = Stream.query(Stream.name==stream_name)
        streams = stream_query.fetch(1)
        stream = streams[0]
        t = datetime.date.today()
        print t.day
        print 'answer~~~'

        geo_info = []
        if stream.photos != None:
            for photo in stream.photos:
                photo_dict = {
                    "filename":photo.filename,
                    "latitude":photo.latitude,
                    "longitude":photo.longitude,
                    "uploadDate":photo.upload_time.strftime("%m/%d/%y"),
                }
                print photo_dict
                geo_info.append(photo_dict)
        print geo_info
        print json.dumps(geo_info)
        template_values={
            'id':stream.key.urlsafe(),
            'geo_info':json.dumps(geo_info),
            'photos_num':len(geo_info),
            'today_date': t.day
        }
        self.response.write(template.render(template_values))
