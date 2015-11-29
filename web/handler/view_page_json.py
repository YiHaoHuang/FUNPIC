import os
import urllib
import time
import datetime
import random
import json
from math import sin, cos, sqrt, atan2, radians

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from stream import *

import webapp2

class ViewPage_json(webapp2.RequestHandler):
    def get(self):
        stream_name = self.request.get('stream_name')
        stream_query = Stream.query(Stream.name==stream_name)
        streams = stream_query.fetch(1)
        stream = streams[0]
        json_dict = {"displayImages":[],"imageCaptionList":[],"author":[]}

        if stream.photos != None:
            url="http://even-hull-108219.appspot.com/"
            for idx in range(len(stream.photos)):
                photo = stream.photos[idx]
                json_dict['displayImages'].append(url+"img?img_id=%s&img_idx=%s"%(stream.key.urlsafe(),str(idx)))
                json_dict['imageCaptionList'].append(photo.filename)
                json_dict['author'].append(stream.author.email.lower())
            json_dict['displayImages'].reverse()
            json_dict['imageCaptionList'].reverse()
        self.response.write(json.dumps(json_dict))

class GetUploadURL(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/uploadphoto_json')
        upload_url = str(upload_url)
        dictPassed = {'upload_url':upload_url}
        jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)

class UploadPhoto_json(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        stream_name = self.request.params['stream_name']
        stream_query = Stream.query(Stream.name==stream_name)
        streams = stream_query.fetch(1)
        stream = streams[0]

        filename = self.request.params['filename']

        #img = images.resize(img, 200, 200)

        stream.photos.append(Photo(
                blob_key = upload.key(),
                filename=filename,
                latitude=float(self.request.params['latitude']),
                longitude=float(self.request.params['longitude'])
        ))
        stream.last_date=datetime.datetime.now()
        stream.put()
        time.sleep(1)

class NearBy_json(webapp2.RequestHandler):
    def get(self):
        latitude = float(self.request.get('latitude'))
        longitude = float(self.request.get('longitude'))
        photo_list = []
        streams = Stream.query()
        url="http://even-hull-108219.appspot.com/"
        for stream in streams:
            for idx in range(len(stream.photos)):
                photo = stream.photos[idx]
                photo_dict={'distance':self.calDistance(latitude,longitude,photo.latitude,photo.longitude),
                            'stream_name':stream.name,
                            'url':url+"img?img_id=%s&img_idx=%s"%(stream.key.urlsafe(),str(idx))
                            }
                photo_list.append(photo_dict)
        photo_list = sorted(photo_list, key=lambda k: k['distance'])
        # json_dict={"distance":[ '%.1fkm'%photo['distance'] for photo in photo_list],
        #            "stream_name":[ photo['stream_name'] for photo in photo_list],
        #            "url":[ photo['url'] for photo in photo_list]}
        json_dict = {"distance":[],"stream_name":[],"url":[]}
        for photo in photo_list:
            json_dict["stream_name"].append(photo['stream_name'])
            json_dict["url"].append(photo['url'])
            if photo['distance']<9999:
                json_dict["distance"].append('%.1fkm'%photo['distance'])
            else:
                json_dict["distance"].append('%.0fkm'%photo['distance'])

        self.response.write(json.dumps(json_dict))


    def calDistance(self,lat1,lon1,lat2,lon2):
        R = 6373.0
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance



