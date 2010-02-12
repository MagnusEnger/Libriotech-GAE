from google.appengine.ext import db
from google.appengine.tools import bulkloader

class BokhyllaItem(db.Model):
  no = db.IntegerProperty()
  urn = db.ListProperty(unicode)
  oaiid = db.ListProperty(unicode)
  sesamid = db.ListProperty(unicode)
  isbn = db.ListProperty(unicode)
  pages = db.IntegerProperty()
  title = db.StringProperty(unicode)
  creator = db.StringProperty(unicode)
  ticr = db.StringProperty(unicode)
  public = db.BooleanProperty()
  bokhylla = db.BooleanProperty()
  date_added = db.DateTimeProperty(auto_now_add=True)
  last_modified = db.DateTimeProperty(auto_now=True)

def make_list(s):
  try:
    s = unicode(s, "utf_8")
    return s.split(",")
  except:
    return []

def make_string(s):
  try: 
    return unicode(s, "utf_8")
  except:
  	return ""

def make_int(s):
  if s.isdigit():
    return int(s)
  else:
    return 0

def bool_from_string(s):
  if s == 'true':
    return True
  else:
    return False

class BokhyllaItemLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'BokhyllaItem',
                                   [('no', int), 
                                    ('urn', make_list),
                                    ('oaiid', make_list),
                                    ('sesamid', make_list),
                                    ('isbn', make_list), 
                                    ('pages', make_int), 
                                    ('title', make_string), 
                                    ('creator', make_string), 
                                    ('ticr', make_string), 
                                    ('public', bool_from_string), 
                                    ('bokhylla', bool_from_string)
                                   ])

  def generate_key(self, i, values):
    return values[0]

loaders = [BokhyllaItemLoader]