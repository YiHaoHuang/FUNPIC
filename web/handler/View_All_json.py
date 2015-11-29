import os
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from stream import *

import jinja2
import json
import webapp2

class View_All_json(webapp2.RequestHandler):
    def get(self):
        stream_all_indexed = Stream.query().order(-Stream.last_date).fetch(16)

        stream = stream_all_indexed[0]
        json_dict = {"displayImages":[],"imageCaptionList":[]}

        if stream_all_indexed[0] != None:
            url="http://even-hull-108219.appspot.com/"
            for idx in range(len(stream_all_indexed)):
                cover_url = stream_all_indexed[idx].cover_url
                if cover_url=='':
                    cover_url = "http://www.sdpb.org/s/photogallery/img/no-image-available.jpg"
                name = stream_all_indexed[idx].name
                json_dict['displayImages'].append(cover_url)
                json_dict['imageCaptionList'].append(name)

        jsonObj = json.dumps(json_dict, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)
