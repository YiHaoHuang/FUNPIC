import os
import urllib, cStringIO
import time
import datetime
import random

import colorsys
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api.images import get_serving_url
from stream import *
import PIL.Image
import PIL.ImageFilter
import PIL.ImageEnhance
import jinja2
import webapp2
import operator
from numpy import *


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class edit(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('template/edit_page.html')
        if not users.get_current_user():
            self.redirect('/')
        stream_name_real = self.request.get('stream_name')
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        img2_first  = self.request.get('img2_first')
        print edit_first
        print img2_first
        print "OMGGGGGGGGGGGGGGGG"
        print stream_name_real
        stream = stream_key.get()
        stream_name = stream.photos[int(img_idx)].filename
        print int(img_idx)
        print stream_key
        template_values = {
            'name':stream_name,
            'stream_name_real':stream_name_real,
            'id': stream.key.urlsafe(),
            'idx': int(img_idx),
            'edit_first': int(edit_first),
            'img2_first': int(img2_first)
        }
        self.response.write(template.render(template_values))

class save_original(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')
        stream_name = self.request.get('stream_name')
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(0)
        img2_first = int(0)
        stream = stream_key.get()
        URL = 'http://funpic-1119.appspot.com/img?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)
        print URL
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos_original:
            stream.photos_original=[]

        stream.photos_original.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))
        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class save_new_photo(webapp2.RequestHandler):
    def post(self):
        if not users.get_current_user():
            self.redirect('/')

        stream_name_real = self.request.get('stream_name_real')
        stream_query = Stream.query(Stream.name==stream_name_real)
        streams = stream_query.fetch(1)
        stream = streams[0]

        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        img2_first  = self.request.get('img2_first')
        print img2_first
        edit_first =int(1)

        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file).convert('L')
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()
        print "PPPPPPPPPPPPPPPPPPPPPPPPP"
        print len(stream.photos)
        stream.photos.append(Photo(
                    image=data,
                    filename='new photo',
                    comment='grayscale',
                    latitude=random.uniform(-90.0,90.0),
                    longitude=random.uniform(-180.0,180.0)
                    ))
        print len(stream.photos)
        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        print '/ViewPage?stream_name='+str(stream_name_real)
        self.redirect('/viewpage?stream_name='+str(stream_name_real))

class Image2(webapp2.RequestHandler):
    def get(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        print img_idx
        stream = stream_key.get()
        print 'hiii'
        print stream_key
        print stream.photos2
        ## from goole API
        img2_first  = self.request.get('img2_first')
        print img2_first
        print int(img2_first)
        print "POPO"
        if int(img2_first) >0:
            img = images.Image(stream.photos2[0].image)
            print stream.photos2[0].blob_key
            print 'WTFFFF'
            if stream.photos2:
                if stream.photos2[0].blob_key != None:
                    print '111'
                    self.redirect(images.get_serving_url(stream.photos2[1].blob_key))
                else:
                    print '222'
                    self.response.headers['Content-Type'] = 'image/jpeg'
                    self.response.out.write(stream.photos2[0].image)
            else:
                return
                self.response.out.write('No image')
        else:
            print "GGGININ"
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(stream.photos_original[0].image)
            print img2_first

class recover(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')

        stream = stream_key.get()
        img = stream.photos_original[0].image
        print type(img)
        stream.photos2=[]



        stream.photos2.append(Photo(
                image=img,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&stream_name='+str(stream_name_real)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))



class grayscale(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        print "POPKSKJDKASJDAL:DJ"
        print stream_name_real
        print img2_first
        edit_first =int(1)

        stream = stream_key.get()
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file).convert('L')
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()
        print "@@@@@@@@@@@@@@"
        if stream.photos2:
            print "WTTFFF"
            stream.photos2=[]
        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))
        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class binary(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        im = PIL.Image.open(file)

        ld = im.load()
        width, height = im.size
        print ld[20,25]
        print '=============='
        print '==============='
        for y in range(height):
            for x in range(width):
                r,g,b = ld[x,y]
                h,s,v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
                if s>0.5:
                   ld[x,y] = (0,0,0)
                else:
                   ld[x,y] = (255,255,255)

        buf = cStringIO.StringIO()
        im.save(buf, "JPEG")
        data = buf.getvalue()
        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class contour(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.CONTOUR)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class gaussianblur(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.GaussianBlur)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class MedianFilter(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.MedianFilter(5))
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class SHARPEN(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.SHARPEN)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class brighter(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        enhancer = PIL.ImageEnhance.Brightness(img2)
        img3 = enhancer.enhance(2.0)
        buf = cStringIO.StringIO()
        img3.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class Darker(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        enhancer = PIL.ImageEnhance.Brightness(img2)
        img3 = enhancer.enhance(0.5)
        buf = cStringIO.StringIO()
        img3.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class EMBOSS(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.EMBOSS)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class EDGE_ENHANCE(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.EDGE_ENHANCE_MORE)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class AverageFilter(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.Kernel((5, 5), [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class Highpass(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.Kernel((3, 3), [-1.0/8.0,-1.0/8.0,-1.0/8.0,-1.0/8.0,16.0/8.0,-1.0/8.0,-1.0/8.0,-1.0/8.0,-1.0/8.0]))
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class Edge_Detection(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.filter(PIL.ImageFilter.Kernel((3, 3), [0,1,0,-1,4,-1,0,-1,0]))
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class rotate(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file)
        img2 = img2.rotate(90)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class invert(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())

        img3 = array(PIL.Image.open(file).convert('L'))
        img4 = 255 - img3
        pil_im = PIL.Image.fromarray(img4)
        buf = cStringIO.StringIO()
        pil_im.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class narrow(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())

        img3 = array(PIL.Image.open(file).convert('L'))
        img4 = (100.0/255) * img3 + 100
        pil_im = PIL.Image.fromarray(uint8(img4))
        buf = cStringIO.StringIO()
        pil_im.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

class squared(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())

        img3 = array(PIL.Image.open(file).convert('L'))
        img4 = 255.0 * (img3/255.0)**2
        pil_im = PIL.Image.fromarray(uint8(img4))
        buf = cStringIO.StringIO()
        pil_im.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))

def equalize(h):
    lut = []
    for b in range(0, len(h), 256):

        # step size
        step = reduce(operator.add, h[b:b+256]) / 255

        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + h[i+b]

    return lut

class FSCS(webapp2.RequestHandler):
    def post(self):
        stream_key = ndb.Key(urlsafe=self.request.get('img_id'))
        img_idx = self.request.get('img_idx')
        edit_first  = self.request.get('edit_first')
        edit_first =int(1)
        stream = stream_key.get()
        img2_first  = self.request.get('img2_first')
        stream_name_real  = self.request.get('stream_name_real')
        URL = 'http://funpic-1119.appspot.com/img2?img_id='+str((stream.key.urlsafe()))+'&img_idx='+str(img_idx)+'&img2_first='+str(img2_first)
        print URL
        img2_first = int(1)
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img2 = PIL.Image.open(file).convert('L')

        # calculate lookup table
        lut = equalize(img2.histogram())

        # map image through lookup table
        img2 = img2.point(lut)
        buf = cStringIO.StringIO()
        img2.save(buf, "JPEG")
        data = buf.getvalue()

        if stream.photos2:
            stream.photos2=[]

        stream.photos2.append(Photo(
                image=data,
                filename='new photo',
                comment='grayscale',
                latitude=random.uniform(-90.0,90.0),
                longitude=random.uniform(-180.0,180.0)
                     ))

        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)
        self.redirect('/edit?img_id='+str((stream.key.urlsafe()))+'&stream_name='+str(stream_name_real)+'&img_idx='+str(img_idx)+'&edit_first='+str(edit_first)+'&img2_first='+str(img2_first))
