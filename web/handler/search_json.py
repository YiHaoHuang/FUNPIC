import os
import json
from stream import *
from check_time import *
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_STREAM_NAME = 'default_stream'
DEFAULT_Save_Cache_NAME = 'default_save_cache'



class search_json(webapp2.RequestHandler):
    def get(self):

        search_tag =()
        stream_merge_list=[]
        if self.request.get('search_tag') != "":
            search_tag = self.request.get('search_tag')
            stream__tag = Stream.query(Stream.tags==search_tag)
            stream_query_tag = stream__tag.fetch()
            stream__name = Stream.query(Stream.name==search_tag)
            stream_query_name = stream__name.fetch()
            stream_merge = stream_query_name+stream_query_tag
            stream_merge_list = []
            seen = set()
            for item in stream_merge:
                if item.name not in seen:
                    stream_merge_list.append(item)
                    seen.add(item.name)

            for test in stream_merge_list:
                print test.name
            print '---------------'
            print type(stream_merge)
            print search_tag

        json_dict = {"displayImages":[],"imageCaptionList":[]}

        if len(stream_merge_list) != 0:
            for tmp in stream_merge_list:
                cover_url = tmp.cover_url
                if cover_url=='':
                    cover_url = "http://www.sdpb.org/s/photogallery/img/no-image-available.jpg"
                name = tmp.name
                json_dict['displayImages'].append(cover_url)
                json_dict['imageCaptionList'].append(name)

        jsonObj = json.dumps(json_dict, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)
