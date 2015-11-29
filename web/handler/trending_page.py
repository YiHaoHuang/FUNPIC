import os
import urllib
import time
import datetime
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from stream import *
from check_time import *

import jinja2
import webapp2
DEFAULT_Check_Time_NAME = 'default_Check_Time'
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class TrendingPage(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        check_time = Check_Time.get_by_id(DEFAULT_Check_Time_NAME)
        if check_time:
            print 'TEST'
        else:
            check_time = Check_Time(id=DEFAULT_Check_Time_NAME)

        # check_time = Check_Time(id=DEFAULT_Check_Time_NAME)
        template = JINJA_ENVIRONMENT.get_template('template/trending_page.html')
        streams = Stream.query().fetch()

        for stream in streams:
            stream.view_history = [ view for view in stream.view_history if datetime.datetime.now()-view < datetime.timedelta(minutes=60)]
            stream.put()

        trending_streams = Stream.query().order(-Stream.history_len).fetch(3)
        frequency_choices = [('1','No report'),('2','Every 5 mins'),('3','Every 1 hour'),('4','Every day')]
        if self.request.get('selected_value')!="":
            selected_value = self.request.get('selected_value')
            check_time.absolute_time=datetime.datetime.now()
            check_time.frequency = selected_value
            check_time.put()
        else:
            selected_value = "1"


        if check_time.absolute_time:
            delta_time = datetime.datetime.now() - check_time.absolute_time
            print '-------'
            print delta_time.seconds
            print '-------'
        else:
            check_time.absolute_time = datetime.datetime.now()
            check_time.frequency="1"

        go=0
        if check_time.frequency=="2":
            if delta_time.seconds >= 300:
                check_time.absolute_time=datetime.datetime.now()
                check_time.put()
                go=1
            else:
                go=0
        elif check_time.frequency=="3":
            if delta_time.seconds >= 3600:
                check_time.absolute_time=datetime.datetime.now()
                check_time.put()
                go=1
            else:
                go=0
        elif check_time.frequency=="4":
            if delta_time.seconds >= 86400:
                check_time.absolute_time=datetime.datetime.now()
                check_time.put()
                go=1
            else:
                go=0
        else:
            print check_time.frequency

        body_email=''
        for body in trending_streams:
            body_email += body.name +': '+ str(body.history_len)+ '\n'


        print go
        print body_email

        if go==1:
            project_id = 'even-hull-108219'
            to = 'ikehuang.yh@gmail.com,liuhsinyu@gmail.com,nima.dini@utexas.edu,kevzsolo@gmail.com'
            subject = 'Top 3 trending streams'
            mail.send_mail(sender="Project Name :: Info <info@" +project_id+ ".appspotmail.com>",
                           to=to,
                           subject=subject,
                           body=body_email)


        template_values = {
            'trending_streams':trending_streams,
            'frequency_choices':frequency_choices,
            'selected_value':selected_value,
        }
        self.response.write(template.render(template_values))

class SendEmail(webapp2.RequestHandler):
    def post(self):
        value = self.request.get('frequency')
        self.redirect('/trending?selected_value='+value)
