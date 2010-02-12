#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os, random

from google.appengine.ext import db, webapp
from google.appengine.ext.db import stats
from google.appengine.ext.webapp import util, template
from django.utils import simplejson

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

class MainHandler(webapp.RequestHandler):

  def get(self):
  
    template_values = {}

    if self.request.get('isbn'):
      isbn = unicode(self.request.get('isbn'))
      isbn = isbn.replace("-", "")
      items = db.GqlQuery("SELECT * FROM BokhyllaItem WHERE isbn = :isbn", isbn=isbn)
      template_values["isbn"] = isbn
    elif self.request.get('no'):
      no = int(self.request.get('no'))
      items = db.GqlQuery("SELECT * FROM BokhyllaItem WHERE no = :no", no=no)
    # Search
    elif self.request.get('q'):
      q = unicode(self.request.get('q'))
      items = db.GqlQuery("SELECT * FROM BokhyllaItem WHERE ticr = :q", q=q)
    elif self.request.get('au'):
      au = unicode(self.request.get('au'))
      items = db.GqlQuery("SELECT * FROM BokhyllaItem WHERE creator = :creator", creator=au)
    elif self.request.get('ti'):
      ti = unicode(self.request.get('ti'))
      items = db.GqlQuery("SELECT * FROM BokhyllaItem WHERE creator = :title", title=ti)
    # By type
    elif self.request.get('coll'):
      coll = unicode(self.request.get('coll'))
      if coll == 'public':
        items = db.GqlQuery("SELECT * FROM BokhyllaItem WHERE public = True ORDER BY no DESC LIMIT 25")
      elif coll == 'bokhylla':
        items = db.GqlQuery("SELECT * FROM BokhyllaItem WHERE bokhylla = True ORDER BY no DESC LIMIT 25")
    else:  
      items = db.GqlQuery("SELECT * FROM BokhyllaItem ORDER BY no DESC LIMIT 25")
        
    if items:
      template_values["items"] = items

    if self.request.get('format') == 'json':
      # Translate items into dicts that can be serialzied as JSON
      jsonitems = []
      for item in items:
        jsonitem = {}
        jsonitem["no"] = unicode(item.no)
        jsonitem["urn"] = list(item.urn)
        jsonitem["oaiids"] = list(item.oaiid)
        jsonitem["sesamids"] = list(item.sesamid)
        jsonitem["isbn"] = list(item.isbn)
        jsonitem["pages"] = unicode(item.pages)
        jsonitem["title"] = unicode(item.title)
        jsonitem["creator"] = unicode(item.creator)
        jsonitem["public"] = unicode(item.public)
        jsonitem["bokhylla"] = unicode(item.bokhylla)
        jsonitem["urn_url"] = []
        jsonitem["pdf_url"] = []
        # Links to Bokhylla based on URN
        for urn in item.urn:
          jsonitem["urn_url"].append("http://www.nb.no/utlevering/contentview.jsf?urn=" + urn)
          if item.public:
            jsonitem["pdf_url"].append("http://www.nb.no/utlevering/pdfbook?id=" + urn[14:])
        jsonitem["bibsys_url"] = []
        # Links to BIBSYS, based on oaiid
        for oaiid in item.oaiid:
          jsonitem["bibsys_url"].append("http://ask.bibsys.no/ask/action/show?pid=" + oaiid[21:] + "&kid=biblio")
        jsonitems.append(jsonitem)
      self.response.out.write(simplejson.dumps(jsonitems))
    else:
      template_values["query_string"] = self.request.query_string
      path = os.path.join(os.path.dirname(__file__), 'tmpl/index.tmpl')
      self.response.out.write(template.render(path, template_values))

class ViewItem(webapp.RequestHandler):

  def get(self):
  
    template_values = {}
    if self.request.get('no'):
      item = BokhyllaItem.get(no)
      template_values = {'item': item}
    else:
      template_values = {'error': "Ingen identifikator angitt."}
      
    path = os.path.join(os.path.dirname(__file__), 'tmpl/index.tmpl')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/bokhylladb/', MainHandler), 
                                        ('/bokhylladb/item/', ViewItem)
                                       ],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
