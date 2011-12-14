import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
import webapp2

from google.appengine.api import users

class SurveyList(db.Model):
  creator = db.UserProperty()
  name = db.StringProperty()
  #content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  
class Survey(db.Expando):
  surveyid = db.StringProperty()
  question = db.StringProperty()
  options =  db.StringListProperty()
  surveyoption = db.BlobProperty()

class Votes(db.Expando):
  surveyid = db.StringProperty()
  voter = db.UserProperty()
  question = db.StringProperty()
  chosenoption = db.StringProperty()


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
            <a href='/edit1'><h3>Edit surveys created by you.</h3></a></div>""")
  
            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/vote'><h3>Vote on the surveys of all the users.</h3></a></div>""")
            
            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/result1'><h3>View results of the surveys.</h3></a></div></style>""")
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
            self.response.out.write("<h3>Survey created. <a href='/Create3'>Click here to go back.</a></h3>")
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

            self.response.out.write("<center>Please select from one of the following surveys:-")
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
            
            duplicatevote=0
                                
            i=1
            j=1
            self.response.out.write("<form name=actualvote action='/vote3' method='POST'>")
            for cntr1 in questionlist:
              oldqueryvote=db.GqlQuery("SELECT * "
                                     "FROM Votes "
                                     "WHERE surveyid=:1 AND voter=:2 AND question=:3", surveyname1, user, cntr1.question)
              self.response.out.write("<br>Q:- %s" % cntr1.question)
              i=1
              
              for cntr2 in cntr1.options:
                alreadythere=0
                for voteiter in oldqueryvote:
                    if voteiter and voteiter.chosenoption==cntr1.options[i-1]:
                          self.response.out.write("<br><input type=radio name=oq%s value=%s checked>%s</input>" % (j,cntr1.options[i-1],cntr1.options[i-1]))
                          alreadythere=1
                          break
                      
                if alreadythere==0:        
                    self.response.out.write("<br><input type=radio name=oq%s value=%s>%s</input>" % (j,cntr1.options[i-1],cntr1.options[i-1]))
                i+=1
              j+=1
              
            #self.response.out.write("<input type=hidden name=hiddennoofques value=%s>" % count(questionlist))
            self.response.out.write("<input type=hidden name=hiddensurveyname value=%s>" % surveyname1)
            self.response.out.write("<br><input type=submit value='Vote'><input type='reset' value='Clear Form'>")                
            self.response.out.write("</form>")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Vote3(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            surveyname1 = self.request.get('hiddensurveyname')
            #noofques = self.request.get('hiddennoofques')
            questionlist = db.GqlQuery("SELECT * "
                                "FROM Survey "
                                "WHERE surveyid=:1 ", surveyname1)
            currentvotes=db.GqlQuery("SELECT * "
                                "FROM Votes "
                                "WHERE surveyid=:1 ", surveyname1)
            self.response.out.write("Viewing survey:- %s" % surveyname1)
            j=1
            duplicatevote=0
            duplicateoccuredever=0
            for crntques in questionlist:
                duplicatevote=0
                currentvote=Votes(voter=user, surveyid=surveyname1, question=crntques.question)
                oq="oq"+str(j)
                currentvote.chosenoption=self.request.get(oq)
                oldquery=db.GqlQuery("SELECT * "
                                     "FROM Votes "
                                     "WHERE surveyid=:1 AND voter=:2 AND question=:3 AND chosenoption=:4 ", surveyname1, user, crntques.question, self.request.get(oq))
                duplicateoccurever=0
                for count9 in oldquery:
                  if currentvote.chosenoption != "" and currentvote.surveyid==count9.surveyid and currentvote.voter==count9.voter and currentvote.question==count9.question and currentvote.chosenoption==count9.chosenoption:
                      if duplicateoccuredever==0:
                          self.response.out.write("<center><h3> If you changed your vote then it has gone through. But I have detected that you are trying to vote multiple times for the same option.  I'm sorry, %s. I'm afraid I can't let you do this.<br> So those votes I won't count again.</h3>" % user.nickname())
                          self. response.out.write("These questions you tried to vote the same option multiple times.")
                      self.response.out.write("<br> %s"% currentvote.question)
                      duplicatevote=1
                      duplicateoccuredever=1
                      
                if duplicatevote == 0:
                    oldquery2=db.GqlQuery("SELECT * "
                                     "FROM Votes "
                                     "WHERE surveyid=:1 AND voter=:2 AND question=:3 ", surveyname1, user, crntques.question)
                    for cntr9 in oldquery2:
                      db.delete(cntr9)
                    currentvote.put()
                j=j+1
                
            if duplicateoccuredever==1:
                  self.response.out.write("<h3>Click the button to go back.</a>")
                  self.response.out.write("<FORM><INPUT TYPE='button' VALUE='Back' onClick='history.go(-1);return true;'></FORM></center>")
                  return
            self.response.out.write("<br>Voting done.<br><a href='/'> Click here to go to main menu.</a>")
            
            

            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Result1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList")
            self.response.out.write("<h2>Viewing Results</h2>")
            self.response.out.write("<center>Please select from one of the following surveys:-")
            #self.response.out.write("<form name=voteform1 action='/voteform2'>")
            for cntr in surveylist:
              self.response.out.write("<br><a href='/result2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
            self.response.out.write("</center>")            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Result2(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            self.response.out.write("<div align=right><br><a href='/'> Click here to go to main menu.</a></div>")
            self.response.out.write("<h2>Viewing Results</h2>")
            surveyname=self.request.get('surveyname')
            questionlist = db.GqlQuery("SELECT * "
                                "FROM Survey "
                                "WHERE surveyid=:1 ", surveyname)
            votelist = db.GqlQuery("SELECT * "
                                "FROM Votes "
                                "WHERE surveyid=:1 ", surveyname)
            self.response.out.write("<br>Viewing survey:- %s" % surveyname)
            #votescollection[0]=0
            #votescollection = []
            for ques in questionlist:
              self.response.out.write("<br><br>Q:- %s" % ques.question)
              #for cntr in range(1,len(ques.options)+1):
              #  votescollection[cntr]=0
              #for cntr in ques.options:
              #  votescollection[cntr]=0
              i=0
              for crntoption in ques.options:
                #i=1
                votescollection = []
                for crntvote in votelist:
                  #self.response.out.write("crntvote is :- %s" % crntvote.question)
                  #self.response.out.write("ques is :- %s" % ques.question)
                  if crntvote.question==ques.question and crntvote.chosenoption==crntoption:
                      votescollection.append(1)
                self.response.out.write("<br>%s %s" % (crntoption, len(votescollection)))
                i+=1
              
            
            votecount=0

            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Edit1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList")
            self.response.out.write("<h2>Selecting Survey to edit.</h2>")
            self.response.out.write("<center>Please select from one of the following surveys:-")
            #self.response.out.write("<form name=voteform1 action='/voteform2'>")
            for cntr in surveylist:
              self.response.out.write("<br><a href='/edit2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
            self.response.out.write("</center>")            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Edit2(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br><br><br><br><br>" % greeting)
            self.response.out.write("<div align=right><br><a href='/'> Click here to go to main menu.</a></div>")
            #self.response.out.write("<h2>Viewing Results</h2>")
            surveyname=self.request.get('surveyname')
            questionlist = db.GqlQuery("SELECT * "
                                "FROM Survey "
                                "WHERE surveyid=:1 ", surveyname)
            #self.response.out.write("<br>Viewing survey:- %s" % surveyname)


            #useimages=cgi.escape(self.request.get('useimageshidden'))
            useimages="n"
            #noofques1=db.GqlQuery("SELECT count(question) "
            #                    "FROM Survey "
            #                    "WHERE surveyid=:1 ", surveyname)
            noofques=0
            for cnts in questionlist:
              noofques+=1
            #self.response.out.write("Hey folks! %s" % noofques)
            for abcd in questionlist:
              noofoptions=int(len(abcd.options))
              break
            #self.response.out.write("<br>Hi %sabc" % useimages)


            dbsurveys = db.GqlQuery("SELECT * "
                            "FROM SurveyList ")
            
            #for cntr in dbsurveys:
            #  if cntr.name == surveyname:
            #    self.response.out.write("<h3>That Survey name --> <b>'%s'</b> has not been created yet, so can't be modified.</h3>" % surveyname)
            #    self.response.out.write("<FORM><INPUT TYPE='button' VALUE='Back' onClick='history.go(-1);return true;'></FORM>")
            #    return;
                
            #newsurvey=SurveyList(creator = users.get_current_user(),name=surveyname)
            #newsurvey.put()
            #self.response.out.write("Done")
            
            self.response.out.write('Modifying Survey:- ')
            self.response.out.write(cgi.escape(self.request.get('surveyname')))
            #noofques = int(cgi.escape(self.request.get('noofques')))
            #noofoptions = int(cgi.escape(self.request.get('noofoptionsperques')))
            #useimages = cgi.escape(self.request.get('useimages'))
            self.response.out.write("""<form name=editform3 action="/edit3" enctype="multipart/form-data" method="post">""")
            #if noofques==6:
             # self.response.out.write(range(noofques))
            #else:
             # self.response.out.write("Hey"+noofques)
            qstnlst = db.GqlQuery("SELECT * "
                                "FROM Survey "
                                "WHERE surveyid=:1 ", surveyname)
            question9 = []
            optionslist = []
            for qcntr in qstnlst:
              question9.append(qcntr.question)
            for qcntr1 in qstnlst:
              for xyz in range(noofoptions):
                  optionslist.append(qcntr1.options[xyz])
              #for qwe in range(quesno)
                #if qwe==quesno:
            i=0
            self.response.out.write("<h5> For those options where you are going to use images, don't write anything in the textbox AND upload the file using 'Choose file' option.</h5>")
            for quesno in range(1,noofques+1):
              self.response.out.write("""Question %s:- <input type=text name=question%s value=%s><br>""" % (quesno,quesno,question9[quesno-1]))                        
              if useimages=="n":                        
                for optionno in range(1,noofoptions+1):
                  self.response.out.write("""Option %s:- <input type=text name=q%soption%s value=%s><br>""" % (optionno,quesno,optionno,optionslist[i]))
                  i+=1
                self.response.out.write("<br><br>")
              elif useimages=="y":
                for optionno in range(1,noofoptions+1):
                  self.response.out.write("""<pre>Option %s:- <input type=text name=q%soption%s>            <input type="file" name=q%soptionfile%s/><br></pre>""" % (optionno,quesno,optionno,quesno,optionno))
                self.response.out.write("<br><br>")
            self.response.out.write("""<input type=hidden name=surveynamehidden value='%s'>""" % (surveyname))
            self.response.out.write("""<input type=hidden name=useimageshidden value=%s>""" % useimages)
            self.response.out.write("""<input type=hidden name=noofoptionshidden value=%s>""" % noofoptions)
            self.response.out.write("""<input type=hidden name=noofqueshidden value=%s>""" % noofques)
            self.response.out.write("""<br><br><input type="submit" value="Modify Survey"><input type="reset" value="Clear Form"></form>""")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Edit3(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s<br><br>" % greeting)
            self.response.out.write('Modifying Survey:- ')
            surveyname=cgi.escape(self.request.get('surveynamehidden'))
            self.response.out.write(surveyname)
            #surveykeylist=db.GqlQuery("SELECT * "
            #                "FROM SurveyList "
            #                "WHERE name=:1",surveyname)
            #for cntr in surveykeylist:
            #  currentsurveykey=cntr.key()
               #self.response.out.write("%s" % cntr.key())
            abc123= db.GqlQuery("SELECT * "
                             "FROM Survey "
                             "WHERE surveyid=:1",surveyname)
            db.delete(abc123)
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
            self.response.out.write("<h3>Survey modified. <a href='/'>Click here to go to main menu..</a></h3>")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    
            
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/create1', Create1),
                               ('/create2', Create2),
                               ('/create3', Create3),
                               ('/img1', Image1),
                               ('/vote', Vote),
                               ('/vote2', Vote2),
                               ('/vote3', Vote3),
                               ('/result1', Result1),
                               ('/result2',Result2),
                               ('/edit1',Edit1),
                               ('/edit2',Edit2),
                               ('/edit3',Edit3)],
                              debug=True)
