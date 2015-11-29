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


class search(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/')

        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)

        print'GOGOGGOGO'
        stream_query_tag = ()
        search_tag =()

        if self.request.get('get_rebuild') =="":
            get_rebuild = 0
        else:
            get_rebuild = 0


        stream_merge_list =[]
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

            if len(stream_merge_list)>5:
                stream_merge_list = stream_merge_list[0:5]

        stream_all = Stream.query()
        stream_all_query = stream_all.fetch()
        keywords_list = []
        for tmp_stream in stream_all_query:
            keywords_list.append(tmp_stream.name)
            if len(tmp_stream.tags)>1:
                for tag in tmp_stream.tags:
                    keywords_list.append(tag)
            if len(tmp_stream.tags)==1:
                keywords_list.append(tmp_stream.tags[0])



        #keywords = dict(zip(['term'], [keywords_list]))


        template_values = {
            'streams_all': stream_all_query,
            'streams_search': stream_merge_list,
            'search_tag': search_tag,
            'num_search': len(stream_merge_list),
            'keywords':json.dumps(save_cache.save_cache),
            'get_rebuild': get_rebuild,
        }

        template = JINJA_ENVIRONMENT.get_template('template/search.html')
        self.response.write(template.render(template_values))


class Get_Tag(webapp2.RequestHandler):
    def post(self):
        search_tag = self.request.get('search_tag')
        self.redirect('/search?search_tag='+search_tag)


class Get_Rebuild(webapp2.RequestHandler):
    def post(self):
        get_rebuild = self.request.get('get_rebuild')
        self.redirect('/savecache?get_rebuild='+get_rebuild)