from google.appengine.api import users
from google.appengine.ext import ndb

class Check_Time(ndb.Model):
    """A main model for representing an individual Stream entry."""

    frequency = ndb.StringProperty(indexed=False)
    absolute_time = ndb.DateTimeProperty()


class Save_cache(ndb.Model):
    save_cache = ndb.GenericProperty(repeated=True)
