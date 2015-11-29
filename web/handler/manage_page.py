import os
import urllib
import time

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


class MainPage(webapp2.RequestHandler):

    def get(self):
        stream_name = self.request.get('guestbook_name',
                                          DEFAULT_STREAM_NAME)
        #template = JINJA_ENVIRONMENT.get_template('mainpage.html')

        user = users.get_current_user()
        if self.request.get('login') =="":
            page = 0
            login=0
        else:
            login= int(self.request.get('login'))
            page=1

        if page==0:
            print '----'
        else:
            if login==1:
                if user:
                    self.redirect('/manage')
                else:
                    self.redirect(users.create_login_url(self.request.uri))
            else:
                if user:
                    self.redirect(users.create_logout_url(self.request.uri))
                else:
                    index = self.request.uri.find('?login=0')
                    url = self.request.uri[0:index]+'?login=1'
                    self.redirect(users.create_login_url(url))
        print login
        print page
        #print users.get_current_user().email()
        #print users.get_current_user().email()
        template_values = {
            'login': login,
        }
        template = JINJA_ENVIRONMENT.get_template('template/mainpage.html')
        self.response.write(template.render(template_values))

class Login(webapp2.RequestHandler):
    def post(self):
        login = self.request.get('login')
        self.redirect('/?login='+login)


class manage(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.

        #Stream2 = Stream.ancestor(Stream_key(DEFAULT_STREAM_NAME))

        stream_query_own = Stream.query(Stream.author.email==users.get_current_user().email())
        stream_query_own2 = Stream.query(Stream.author.email==users.get_current_user().email().lower())
        streams_tmp1= stream_query_own.fetch()
        streams_tmp2= stream_query_own2.fetch()
        stream_merge = streams_tmp1+streams_tmp2
        streams_user = []
        seen = set()
        for item in stream_merge:
            if item.name not in seen:
                streams_user.append(item)
                seen.add(item.name)

        #stream_query_own = Stream.query(ancestor=Stream_key('default_stream'))
        #stream_query_own.ancestor(DEFAULT_STREAM_NAME)
        stream_query_sub = Stream.query(Stream.subscribers==users.get_current_user().email().lower())

        streams_sub_tmp = stream_query_sub.fetch()
        streams_sub =[]
        for test_sun in streams_sub_tmp:
            if test_sun not in streams_user:
                streams_sub.append(test_sun)

        user_email = users.get_current_user().email().lower()

        print len(streams_user)
        print len(streams_sub)
        #print Stream.author.email
        #print Stream.subscribers
        #print users.get_current_user().email()
        for stream in streams_user:
            if stream.author is None:
                print 'it is None'
            else:
                print stream.name

        template_values = {
            'user_email': user_email,
            'streams_user': [{'name':stream.name,'last_date':stream.last_date,'photos_num':len(stream.photos)} for stream in streams_user],
            'streams_sub': [{'author':stream.author.email,'name':stream.name,'last_date':stream.last_date,'photos_num':len(stream.photos),'view_count':stream.view_count} for stream in streams_sub],
        }
        template = JINJA_ENVIRONMENT.get_template('template/manage_page.html')
        self.response.write(template.render(template_values))
        #self.response.write(template.render())

        #ndb.delete_multi(
        #    Stream.query().fetch(keys_only=True)
        #)

class Delete_User(webapp2.RequestHandler):
    def post(self):
        stream_query_own = Stream.query(Stream.author.email==users.get_current_user().email())
        stream_query_own2 = Stream.query(Stream.author.email==users.get_current_user().email().lower())
        streams_tmp1= stream_query_own.fetch()
        streams_tmp2= stream_query_own2.fetch()
        stream_merge = streams_tmp1+streams_tmp2
        streams_user = []
        seen = set()
        for item in stream_merge:
            if item.name not in seen:
                streams_user.append(item)
                seen.add(item.name)

        for deluser in streams_user:
            delete_user = self.request.get(deluser.name)
            if delete_user =="on":
                deluser.key.delete()

        print 'delete users'
        time.sleep(1)
        self.redirect('/manage')

class Delete_Subscriber(webapp2.RequestHandler):
    def post(self):
        stream_query_sub = Stream.query(Stream.subscribers ==users.get_current_user().email().lower())
        streams_sub = stream_query_sub.fetch()
        for delsub in streams_sub:
            delete_sub = self.request.get(delsub.name)
            if delete_sub =="on":
                update_sub = []
                for element in delsub.subscribers:
                    if element != users.get_current_user().email().lower():
                        update_sub.append(element)
                delsub.subscribers = update_sub
                delsub.put()

        time.sleep(1)
        self.redirect('/manage')

class View_All(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        #stream_all = Stream.query()
        #stream_all_query = stream_all.fetch()
        stream_all_indexed = Stream.query().order(-Stream.create_time).fetch()
        template_values = {
            'streams_all': stream_all_indexed,
        }

        template = JINJA_ENVIRONMENT.get_template('template/view_all.html')
        self.response.write(template.render(template_values))

