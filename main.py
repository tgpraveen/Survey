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
  
class Survey(db.Expando):
  surveyid = db.StringProperty()
  question = db.StringProperty()
  options =  db.StringListProperty()
  surveyoption = db.BlobProperty()


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
                  self.response.out.write("""Option %s:- <input type=text name=q%soption%s><br>""" % (optionno,quesno,optionno))
                self.response.out.write("<br><br>")
              elif useimages=="y":
                for optionno in range(1,noofoptions+1):
                  self.response.out.write("""<pre>Option %s:- <input type=text name=q%soption%s>            <input type="file" name=q%soptionfile%s/><br></pre>""" % (optionno,quesno,optionno,quesno,optionno))
                self.response.out.write("<br><br>")
            self.response.out.write("""<input type=hidden name=surveynamehidden value='%s'>""" % (surveyname))
            self.response.out.write("""<input type=hidden name=useimageshidden value=%s>""" % useimages)
            self.response.out.write("""<input type=hidden name=noofoptionshidden value=%s>""" % noofoptions)
            self.response.out.write("""<input type=hidden name=noofqueshidden value=%s>""" % noofques)
            self.response.out.write("""<br><br><input type="submit" value="Create Survey"><input type="reset" value="Clear Form"></form>""")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Image1(webapp2.RequestHandler):
    def get(self):
        greeting1 = db.get(self.request.get("img_id"))
        self.response.out.write("Hi")
        if greeting1.optionpic:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(greeting1.optionpic)
            
        else:
            self.response.out.write("No image")
            
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
            #self.response.out.write("<br>Hi %sabc" % useimages)
            for cntr in range(1,noofques+1):
              currentquesno="question" + str(cntr)
              surveyquestion=Survey(question=cgi.escape(self.request.get(currentquesno)),surveyid=surveyname)
              if useimages == "n":                  
                  for innercntr in range(1,noofoptions+1):
                      currentoption="q"+str(cntr)+"option" + str(innercntr)
                      #self.response.out.write("<br>Hi %s" % currentoption)
                      surveyquestion.options.append(cgi.escape(self.request.get(currentoption)))
                  #self.response.out.write("<br>eoq")
                  surveyquestion.put()
              elif useimages == "y":
                for innercntr in range(1,noofoptions+1):
                      currentoption="q"+str(cntr)+"option" + str(innercntr)
                      surveyquestion.options.append(cgi.escape(self.request.get(currentoption)))
                      if cgi.escape(self.request.get(currentoption)) != "":
                        surveyquestion.options.append(cgi.escape(self.request.get(currentoption)))
                      else:
                        currentoptionfile="q"+cntr+"optionfile" + str(innercntr)
                        optionpic = self.request.get(currentoptionfile)
                        surveyquestion.optionpic = db.Blob(optionpic)
                #self.response.headers['Content-Type'] = "image/png"
                #self.response.out.write(surveyquestion.optionpic)
                surveyquestion.put()


                pict = db.GqlQuery("SELECT * "
                                "FROM Survey ")
                for pictcntr in pict:
                    self.response.out.write("<div><img src='/img1?img_id=%s'></img></div>" % pictcntr.key())
                    #Not working above inserting/showing pics.        
                    #greet = db.get(self.request.get(pictcntr.key()))
                    #self.response.out.write(greet.question)
            self.response.out.write("<h3>Survey created. <a href='/'>Click here to go back.</a></h3>")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Vote(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList")

            self.response.out.write("<center>Please selct from one of the following surveys:-")
            #self.response.out.write("<form name=voteform1 action='/voteform2'>")
            for cntr in surveylist:
              self.response.out.write("<br><a href='/vote2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
            self.response.out.write("</center>")            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Vote2(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            surveyname1 = self.request.get('surveyname')
            self.response.out.write("Viewing survey:- %s" % surveyname1)
            questionlist = db.GqlQuery("SELECT * "
                                "FROM Survey "
                                "WHERE surveyid=:1 ", surveyname1)
            i=1
            j=1
            self.response.out.write("<form name=actualvote action='/vote3'>")
            for cntr1 in questionlist:
              self.response.out.write("<br>Q:- %s" % cntr1.question)
              i=1
              for cntr2 in cntr1.options:
                self.response.out.write("<br><input type=radio name=q%so%s value=%s>%s</input>" % (j,i,cntr1.options[i-1],cntr1.options[i-1]))
                i+=1
              j+=1
            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
            
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/create1', Create1),
                               ('/create2', Create2),
                               ('/create3', Create3),
                               ('/img1', Image1),
                               ('/vote', Vote),
                               ('/vote2', Vote2)],
                              debug=True)
