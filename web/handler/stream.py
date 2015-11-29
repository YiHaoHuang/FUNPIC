from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_STREAM_NAME = 'default_stream'

def Stream_key(stream_name=DEFAULT_STREAM_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('CreateStream', stream_name)

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=True)

class Photo(ndb.Model):
    image = ndb.BlobProperty()
    filename = ndb.StringProperty()
    comment = ndb.StringProperty(indexed=False)
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    upload_time = ndb.DateTimeProperty(auto_now_add=True)
    blob_key = ndb.BlobKeyProperty()

class Stream(ndb.Model):
    """A main model for representing an individual Stream entry."""
    author = ndb.StructuredProperty(Author)
    name = ndb.StringProperty()
    subscribers = ndb.GenericProperty(repeated=True)
    cover_url = ndb.StringProperty(indexed=False)
    tags = ndb.GenericProperty(repeated=True)
    view_count = ndb.IntegerProperty(indexed=False)
    last_date = ndb.DateProperty()
    photos = ndb.StructuredProperty(Photo,repeated=True)
    photos_original = ndb.StructuredProperty(Photo,repeated=True)
    photos2 = ndb.StructuredProperty(Photo,repeated=True)
    view_history = ndb.DateTimeProperty(repeated=True)
    history_len = ndb.ComputedProperty(lambda self: len(self.view_history))
    create_time = ndb.DateTimeProperty(auto_now_add=True)