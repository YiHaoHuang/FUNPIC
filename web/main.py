import os
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from handler.create_page import CreatePage,CreateStream,ErrorPage,Stream_key
from handler.view_page import ViewPage,UploadPhoto,Image,Subscribe,Unsubscribe
from handler.view_page_json import ViewPage_json,UploadPhoto_json,GetUploadURL,NearBy_json
from handler.stream import *
from handler.search import search,Get_Tag,Get_Rebuild
from handler.trending_page import TrendingPage,SendEmail
from handler.social_page import SocialPage
from handler.manage_page import MainPage,manage,Delete_User,View_All,Login,Delete_Subscriber
from handler.geo_page import GeoView
from handler.savecache import savecache
from handler.View_All_json import View_All_json
from handler.search_json import *
from handler.stream_sub_json import *
from handler.edit_page import *

import jinja2
import webapp2

DEFAULT_STREAM_NAME = 'default_stream'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/manage', manage),
    ('/edit', edit),
    ('/grayscale',grayscale),
    ('/MedianFilter',MedianFilter),
    ('/AverageFilter',AverageFilter),
    ('/invert',invert),
    ('/EDGE_ENHANCE',EDGE_ENHANCE),
    ('/SHARPEN',SHARPEN),
    ('/Brighter',brighter),
    ('/EMBOSS',EMBOSS),
    ('/Highpass',Highpass),
    ('/squared',squared),
    ('/Edge_Detection',Edge_Detection),
    ('/narrow',narrow),
    ('/Darker',Darker),
    ('/contour',contour),
    ('/gaussianblur',gaussianblur),
    ('/rotate',rotate),
    ('/savephoto',save_new_photo),
    ('/FSCS',FSCS),
    ('/save_original',save_original),
    ('/recover',recover),
    ('/binary',binary),
    ('/createpage', CreatePage),
    ('/createstream',CreateStream),
    ('/deleteuser',Delete_User),
    ('/deletesubscriber',Delete_Subscriber),
    ('/viewpage',ViewPage),
    ('/viewpage_json',ViewPage_json),
    ('/gettag', Get_Tag),
    ('/viewall',View_All),
    ('/viewall_json',View_All_json),
    ('/search',search),
    ('/search_json',search_json),
    ('/savecache',savecache),
    ('/getrebuild',Get_Rebuild),
    ('/uploadphoto',UploadPhoto),
    ('/uploadphoto_json',UploadPhoto_json),
    ('/nearby_json',NearBy_json),
    ('/uploadHandler',GetUploadURL),
    ('/subscribe',Subscribe),
    ('/unsubscribe',Unsubscribe),
    ('/img',Image),
    ('/img2',Image2),
    ('/login',Login),
    ('/error',ErrorPage),
    ('/trending',TrendingPage),
    ('/sendemail',SendEmail),
    ('/social',SocialPage),
    ('/geo',GeoView),
    ('/streamsub_json',Stream_sub_json),
], debug=True)