import os
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from stream import *

import json
import jinja2
import webapp2

DEFAULT_STREAM_NAME = 'default_stream'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Stream_sub_json(webapp2.RequestHandler):
    def get(self):

        email_from_web = self.request.get('webemail')

        stream_query_own = Stream.query(Stream.author.email ==email_from_web)
        stream_query_sub = Stream.query(Stream.subscribers ==email_from_web)
        streams_user = stream_query_own.fetch()
        streams_sub_tmp = stream_query_sub.fetch()
        streams_sub =[]
        json_dict = {"displayImages":[],"imageCaptionList":[]}
        for test_sun in streams_sub_tmp:
            if test_sun not in streams_user:
                if len(streams_sub)<16:
                    streams_sub.append(test_sun)
                    json_dict['displayImages'].append(test_sun.cover_url)
                    json_dict['imageCaptionList'].append(test_sun.name)


        jsonObj = json.dumps(json_dict, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)

