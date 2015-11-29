import os
import urllib, cStringIO
import time
import datetime
import random


from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api.images import get_serving_url
from stream import *
import PIL.Image


# response = requests.get(url)
# img = Image.open(StringIO(response.content))

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ViewPage(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('template/view_page.html')
        if not users.get_current_user():
            self.redirect('/')

        stream_name = self.request.get('stream_name')
        stream_query = Stream.query(Stream.name==stream_name)
        streams = stream_query.fetch(1)
        stream = streams[0]

        if stream.photos == None:
            photo_num = 0
        else:
            photo_num = len(stream.photos)
        print photo_num
        start_idx = 0
        end_idx = 0
        if self.request.get('show') == "":
            if self.request.get('notViewed') == "" and ( users.get_current_user() is None or stream.author.email.lower() != users.get_current_user().email().lower()):
                stream.view_history.append(datetime.datetime.now())
                stream.view_count+=1
                stream.put()
            if photo_num == 0:
                start_idx = -1
                end_idx = -1
            else:
                start_idx = photo_num-1
                end_idx = start_idx-min(3,len(stream.photos))
        elif self.request.get('show') == "next":
            start_idx = int(self.request.get('end_idx'))
            end_idx = max(start_idx-3,-1)
        else:
            end_idx = int(self.request.get('start_idx'))
            start_idx = min(end_idx+3,photo_num-1)
        img_names = []
        if start_idx-end_idx>0:
            for idx in range(start_idx,end_idx,-1):
                img_names.append(stream.photos[idx].filename)
        print img_names
        print start_idx
        print end_idx
        print (stream.key.urlsafe())

        # blob_reader = blobstore.BlobReader(blob_key)
        # img = Image.open(blob_reader)
        # file = cStringIO.StringIO(urllib.urlopen('http://funpic-1119.appspot.com/img?img_id=aghkZXZ-Tm9uZXIOCxIGU3RyZWFtIgJHRww&img_idx=1').read())
        # img = Image.open(file)
        # file = cStringIO.StringIO(urllib.urlopen('http://localhost:8080/img?img_id=aghkZXZ-Tm9uZXIOCxIGU3RyZWFtIgJHRww&img_idx=1').read())
        # img = Image.open(file)

        upload_display='display:none;'
        subscribe_display='display:none;'
        subscribe_value=''
        if users.get_current_user() and stream.author.email.lower() == users.get_current_user().email().lower():
            upload_display='display:block;'
            subscribe_display='display:none;'
            subscribe_value=''
        elif users.get_current_user():
            if users.get_current_user().email().lower() in stream.subscribers:
                subscribe_value='unsubscribe'
            else:
                subscribe_value='subscribe'
            upload_display='display:none;'
            subscribe_display='display:block;'
        print zip(range(start_idx,end_idx,-1),img_names)
        template_values = {
            'stream_name':stream_name,
            'id':stream.key.urlsafe(),
            'img_indices':zip(range(start_idx,end_idx,-1),img_names),
            'start_idx':start_idx,
            'end_idx':end_idx,
            'photo_start':len(stream.photos)-1,
            'upload_display':upload_display,
            'subscribe_display':subscribe_display,
            'subscribe_value':subscribe_value,
        }
        self.response.write(template.render(template_values))

class UploadPhoto(webapp2.RequestHandler):
    def post(self):
        stream_name = self.request.get('stream_name')
        stream_query = Stream.query(Stream.name==stream_name)
        streams = stream_query.fetch(1)
        stream = streams[0]
        img = self.request.get('file')
        print 'done'
        if img == '':
            self.error(409)
            self.redirect('/error?error=2&stream_name='+stream_name)
        else:
            print '??'
            print type(img)
            img = images.resize(img, 350, 350)
            # img.im_feeling_lucky()
            print type(img)
            stream.photos.append(Photo(
                    image=img,
                    filename=self.request.POST['file'].filename,
                    comment=self.request.get('comment'),
                    latitude=random.uniform(-90.0,90.0),
                    longitude=random.uniform(-180.0,180.0)
                    ))
            print self.request.POST['file'].filename

            # For upload 2
            # # read from PIL
            # URL = 'http://localhost:8080/img?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(1)
            # print URL
            # URLL= 'https://upload.wikimedia.org/wikipedia/zh/c/c6/Chibi_Maruko-chan.jpg'
            # file = cStringIO.StringIO(urllib.urlopen(URL).read())
            # img2 = PIL.Image.open(file).convert('L')
            # # write from PIL
            # buf = cStringIO.StringIO()
            # img2.save(buf, "JPEG")
            # data = buf.getvalue()
            # print '??????????'
            #
            # stream.photos.append(Photo(
            #         image=data,
            #         filename=self.request.POST['file'].filename,
            #         comment=self.request.get('comment'),
            #         latitude=random.uniform(-90.0,90.0),
            #         longitude=random.uniform(-180.0,180.0)
            #         ))

            stream.last_date=datetime.datetime.now()
            stream.put()
            time.sleep(1)
            self.redirect('/viewpage?stream_name='+stream_name+'&notViewed=True')

class Image(webapp2.RequestHandler):
    def get(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        stream = stream_key.get()

        ## from goole API
        img = images.Image(stream.photos[int(img_idx)].image)
        # imageW = img.size[0]
        # imageH = img.size[1]
        #
        # print imageW
        # print imageH
        # print 'size'
        img.horizontal_flip()
        thumbnail = img.execute_transforms(output_encoding=images.JPEG)

        # im = Image.open(thumbnail)
        print (stream.photos[int(img_idx)].blob_key)
        print self.request.get('img_id')
        # URL = 'http://funpic-1119.appspot.com/img?img_id='+str(self.request.get('img_id'))+'&img_idx='+str(img_idx)
        # URL = 'http://localhost:8080/img?img_id='+str(self.request.get('img_id'))+'&img_idx='+str(img_idx)

        ## PIL load ndb
        URLL= 'https://upload.wikimedia.org/wikipedia/zh/c/c6/Chibi_Maruko-chan.jpg'
        file = cStringIO.StringIO(urllib.urlopen(URLL).read())
        img = PIL.Image.open(file).convert('L')

        # logo = stream.photos[int(img_idx)].image
        # im = PIL.Image.open(logo.open()).convert('L')

        ## PIL show
        buf = cStringIO.StringIO()
        img.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos:
            if stream.photos[int(img_idx)].blob_key != None:
                print '111'
                self.redirect(images.get_serving_url(stream.photos[int(img_idx)].blob_key))
            else:
                print '222'
                self.response.headers['Content-Type'] = 'image/jpeg'
                # self.response.out.write(stream.photos[int(img_idx)].image)
                self.response.out.write(thumbnail)
                #self.response.out.write(data)
        else:
            return
            self.response.out.write('No image')

class Subscribe(webapp2.RequestHandler):
    def post(self):
        stream_name = self.request.get('stream_name')
        stream_query = Stream.query(Stream.name==stream_name)
        streams = stream_query.fetch(1)
        stream = streams[0]
        if users.get_current_user():
            if users.get_current_user().email().lower() not in stream.subscribers:
                stream.subscribers.append(users.get_current_user().email().lower())
        stream.put()
        time.sleep(1)
        self.redirect('/viewpage?stream_name='+stream_name+'&notViewed=True')

class Unsubscribe(webapp2.RequestHandler):
    def post(self):
        stream_name = self.request.get('stream_name')
        stream_query = Stream.query(Stream.name==stream_name)
        streams = stream_query.fetch(1)
        stream = streams[0]
        if users.get_current_user():
            update_sub = []
            for element in stream.subscribers:
                if element != users.get_current_user().email().lower():
                    update_sub.append(element)
            stream.subscribers = update_sub
            stream.put()
            time.sleep(1)
        self.redirect('/viewpage?stream_name='+stream_name+'&notViewed=True')