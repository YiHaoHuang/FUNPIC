import os
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from stream import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class SocialPage(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('template/social_page.html')
        self.response.write(template.render())