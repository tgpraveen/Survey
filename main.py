import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
import webapp2

from google.appengine.api import users

class SurveyList(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  creator = db.UserProperty()
  name = db.StringProperty()
  #content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  
class Survey(db.Model):
  surveyid = db.StringProperty()
  question = db.StringProperty()
  option =  db.StringListProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            
            self.response.out.write("""<br><br><br><br><br><br><div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/create1'><h3>Create a new survey.</h3></a></div></style>""")

            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/edit'><h3>Edit surveys created by you.</h3></a></div>""")
  
            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/vote'><h3>Vote on/View results of the surveys of all the users.</h3></a></div>""")
            self.response.out.write("</body></html>") 
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
class Create1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            self.response.out.write("""<form name=createform1 action="/create2" method="post">
            Enter the survey name:- <input type="text" name=surveyname>
            <br>Will you be using images as any of your survey answers? <input type=radio name=useimages value="n" checked> No
            <input type=radio name=useimages value="y"> Yes
            <br>Number of questions? <input type="text" name=noofques>
            <br>Number of options for each question? <input type="text" name=noofoptionsperques>
            
            
            <br><br><input type="submit" value="Create Survey"><input type="reset" value="Clear Form"></form>""")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Create2(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br>" % greeting)
            surveyname =cgi.escape(self.request.get('surveyname'))
            dbsurveys = db.GqlQuery("SELECT * "
                            "FROM SurveyList ")
            
            for cntr in dbsurveys:
              if cntr.name == surveyname:
                self.response.out.write("<h3>That Survey name --> <b>'%s'</b> is already used please some other survey name.</h3>" % surveyname)
                self.response.out.write("<FORM><INPUT TYPE='button' VALUE='Back' onClick='history.go(-1);return true;'></FORM>")
                return;
                
            newsurvey=SurveyList(creator = users.get_current_user(),name=surveyname)
            newsurvey.put()
            #self.response.out.write("Done")
            
            self.response.out.write('Creating Survey:- ')
            self.response.out.write(cgi.escape(self.request.get('surveyname')))
            noofques = int(cgi.escape(self.request.get('noofques')))
            noofoptions = int(cgi.escape(self.request.get('noofoptionsperques')))
            useimages = cgi.escape(self.request.get('useimages'))
            self.response.out.write("""<form name=createform2 action="/create3" enctype="multipart/form-data" method="post">""")
            #if noofques==6:
             # self.response.out.write(range(noofques))
            #else:
             # self.response.out.write("Hey"+noofques)
            self.response.out.write("<h5> For those options where you are going to use images, don't write anything in the textbox AND upload the file using 'Choose file' option.</h5>")
            for quesno in range(1,noofques+1):
              self.response.out.write("""Question %s:- <input type=text name=question%s><br>""" % (quesno,quesno))                        
              if useimages=="n":                        
                for optionno in range(1,noofoptions+1):
                  self.response.out.write("""Option %s:- <input type=text name=option%s><br>""" % (optionno,optionno))
                self.response.out.write("<br><br>")
              elif useimages=="y":
                for optionno in range(1,noofoptions+1):
                  self.response.out.write("""<pre>Option %s:- <input type=text name=option%s>            <input type="file" name=optionfile%s/><br></pre>""" % (optionno,optionno,optionno))
                self.response.out.write("<br><br>")
            self.response.out.write("""<input type=hidden name=surveynamehidden value='%s'>""" % (surveyname))
            self.response.out.write("""<input type=hidden name=useimageshidden value=%s>""" % useimages)
            self.response.out.write("""<input type=hidden name=noofoptionshidden value=%s>""" % noofoptions)
            self.response.out.write("""<input type=hidden name=noofqueshidden value=%s>""" % noofques)
            self.response.out.write("""<br><br><input type="submit" value="Create Survey"><input type="reset" value="Clear Form"></form>""")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Create3(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br>" % greeting)
            self.response.out.write('Creating Survey:- ')
            surveyname=cgi.escape(self.request.get('surveynamehidden'))
            self.response.out.write(surveyname)
            #surveykeylist=db.GqlQuery("SELECT * "
            #                "FROM SurveyList "
            #                "WHERE name=:1",surveyname)
            #for cntr in surveykeylist:
            #  currentsurveykey=cntr.key()
               #self.response.out.write("%s" % cntr.key())

            useimages=cgi.escape(self.request.get('useimageshidden'))
            noofques=int(cgi.escape(self.request.get('noofqueshidden')))
            noofoptions=int(cgi.escape(self.request.get('noofoptionshidden')))
            for cntr in range(1,noofques+1):
              surveyquestion=Survey(question=cgi.escape(self.request.get('questioncntr')))
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/create1', Create1),
                               ('/create2', Create2),
                               ('/create3', Create3)],
                              debug=True)
