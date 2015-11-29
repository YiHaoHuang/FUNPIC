import os
import urllib

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb

import time
import jinja2
import webapp2
from view_page import ViewPage,UploadPhoto,Image
from stream import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_STREAM_NAME = 'default_stream'


class CreatePage(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('template/create_page.html')
        self.response.write(template.render())

class CreateStream(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('stream_name')
        entity = Stream.get_by_id(name)
        if entity:
            self.error(409)
            self.redirect('/error?error=1')
        else:
            stream = Stream(id=name)
            #stream = Stream(parent=Stream_key(name))
            stream.cover_url = self.request.get('cover_url')
            stream.name = self.request.get('stream_name')
            tmp_subscribers = self.request.get('subscribers').split(',')
            option_msg = self.request.get('option_msg')
            tmp_tags = self.request.get('tags').split(',')
            stream_subscribers = []
            to = ''
            if tmp_subscribers[0] !="":
                for tmp_subscriber in tmp_subscribers:
                    tmp_subscriber = tmp_subscriber.rstrip()
                    tmp_subscriber = tmp_subscriber.lstrip()
                    stream_subscribers.append(tmp_subscriber)
                    if len(to)>0:
                        to += ',' +tmp_subscriber
                    else:
                        to = tmp_subscriber
            stream.subscribers = stream_subscribers

            stream_tags = []
            for tmp_tag in tmp_tags:
                tmp_tag = tmp_tag.rstrip()
                tmp_tag = tmp_tag.lstrip()
                stream_tags.append(tmp_tag)
            stream.tags = stream_tags
            stream.view_count = 0
            if users.get_current_user():
                stream.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
            stream.put()
            time.sleep(1)

            # print len(tmp_subscribers)
            # for test in tmp_subscribers:
            #     print test
            #
            if tmp_subscribers[0] !="":
                project_id = 'even-hull-108219'
                subject = stream.name+' has invited you to view bar!'
                mail.send_mail(sender="Project Name :: Info <info@" +project_id+ ".appspotmail.com>",
                               to=to,
                               subject=subject,
                               body=option_msg)

            self.redirect('/manage')

class ErrorPage(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('template/error_page.html')
        error_code = self.request.get('error')
        error_msgs = {
            '1': "You tried to create a new stream whose name is the same as an existing stream.",
            '2': "You tried to upload empty photo."
        }
        direct_page = {
            '1':'createpage',
            '2':'viewpage?stream_name='+self.request.get('stream_name'),
        }
        template_values = {
            'error_msg':error_msgs[error_code],
            'direct_page':direct_page[error_code]
        }
        self.response.write(template.render(template_values))

