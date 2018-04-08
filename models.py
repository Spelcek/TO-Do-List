from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    opravilo=ndb.StringProperty()
    avtor=ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)



