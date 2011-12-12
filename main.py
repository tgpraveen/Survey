import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
import webapp2

from google.appengine.api import users

class Survey(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  creator = db.UserProperty()
  name = db.StringProperty()
  #content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
            
            self.response.out.write("""<br><br><br><br><br><br><div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/create'><h3>Create a new survey.</h3></a></div></style>""")

            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/edit'><h3>Edit surveys created by you.</h3></a></div>""")

            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/vote'><h3>Vote on/View results of the surveys of all the users.</h3></a></div>""")
     
        else:
            self.redirect(users.create_login_url(self.request.uri))
        

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
