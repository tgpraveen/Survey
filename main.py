import cgi
import datetime
import urllib
import webapp2

import datetime
import time

from google.appengine.ext import db
from google.appengine.api import users
import webapp2

from google.appengine.api import mail
from google.appengine.api import users

class SurveyList(db.Expando):
  creator = db.UserProperty()
  name = db.StringProperty()
  #content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  expirydate = db.DateTimeProperty()
  
  
class Survey(db.Expando):
  surveyid = db.StringProperty()
  question = db.StringProperty()
  options =  db.StringListProperty()
  surveyoption = db.BlobProperty()
  usercomment = db.StringProperty(default="n")

class Votes(db.Expando):
  surveyid = db.StringProperty()
  voter = db.UserProperty()
  question = db.StringProperty()
  chosenoption = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

class Friends(db.Expando):
  user1 = db.StringProperty()
  friends = db.StringListProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")   
            
            self.response.out.write("""<form name='searchform' action='/search1' method='POST'><div align=right><h3>Search for a survey:- <br><input type='text' name='searchword'><br><input type='submit' value='Search'> </h3></div></form>""") 
            
            self.response.out.write("""<br><br><br><br><br><br><div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/create1'><h3>Create a new survey.</h3></a></div></style>""")

            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/edit1'><h3>Edit surveys created by you.</h3></a></div>""")
  
            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/vote'><h3>Vote on the surveys of all the users.</h3></a></div>""")
            
            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/result1'><h3>View results of the surveys.</h3></a></div></style>""")

            self.response.out.write("""<div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/friend1'><h3>View/Add Friends</h3></a></div></style>""")

            if user.nickname()=="test@example.com":
              self.response.out.write("""<br><br><br><br><br><br><div style="float:left;"><h2>Special ADMINISTRATOR Section :- </h2></div></style>""")
              self.response.out.write("""<br><br><br><br><br><br><div style="float:left;text-align: center;background-image: url('/stylesheets/rounded_fixed.gif'); width: 228px; height: 160px; padding: 10px;">
            <a href='/adminedit1'><h3>Edit the survey created by ANY user.</h3></a></div></style>""")
            
            self.response.out.write("</body></html>") 
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class Friend1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            self.response.out.write("<h3><a href='/addfriend1'>Add friends</a></h3>")
            
            currentfriends=db.GqlQuery("SELECT * "
                            "FROM Friends "
                            "WHERE user1=:1", user.nickname())
            initialwritten=0
                           
            for cntr1 in currentfriends:
                for cntr2 in cntr1.friends:
                    if initialwritten==0:
                        self.response.out.write("<br> Current friends:- <br>")
                        initialwritten=1
                    self.response.out.write("<br>%s" % cntr2)
            if initialwritten==0:
              self.response.out.write("It seems you have not added any friends till now. Click the above button to add a few friends. then you can share surveys with only your friends.")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class AddFriend1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            #self.response.out.write("""<h3>To add more friends.</h3>""")
            self.response.out.write("""<br>Leave the field blank if you don't want to add so many friends.<br>""")
            self.response.out.write("""<form name=addfriend1form action="/addfriend2" enctype="multipart/form-data" method="post">""")
            self.response.out.write("""<br>Enter email address of friend 1 <input type=text name=addfriendno1>""")
            self.response.out.write("""<br>Enter email address of friend 2 <input type=text name=addfriendno2>""")
            self.response.out.write("""<br>Enter email address of friend 3 <input type=text name=addfriendno3>""")
            self.response.out.write("""<br><br><input type="submit" value="Add friends"><input type="reset" value="Clear Form"></form>""")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class AddFriend2(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            #self.response.out.write("""<h3>To add more friends.</h3>""")                                       
            friend1=cgi.escape(self.request.get('addfriendno1'))
            friend2=cgi.escape(self.request.get('addfriendno2'))
            friend3=cgi.escape(self.request.get('addfriendno3'))
            #self.response.out.write("<br>%s" % friend1)
            #self.response.out.write("<br>%s" % friend2)
            #self.response.out.write("<br>%s" % friend3)
            addfriend=Friends(user1=user.nickname())
            if friend1!="":
                addfriend.friends.append(friend1)
            if friend2!="":
                addfriend.friends.append(friend2)
            if friend3!="":
                addfriend.friends.append(friend3)
            addfriend.put()
            self.response.out.write("""<h3>Operation completed successfully. <br><br> To add more friends:- <a href='/addfriend1'>Click here</a></h3>""")
            self.response.out.write("""<h3>To view your friends:- <a href='/friend1'>Click here</a></h3>""")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

        
class Create1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            self.response.out.write("""<form name=createform1 action="/create2" method="post">
            Enter the survey name:- <input type="text" name=surveyname>
            <br>Only allow friends to vote on this survey?<input type=radio name=restrictvote value="n" checked> No
            <input type=radio name=restrictvote value="y"> Yes
            <br>Only allow friends to view the results of this survey? <input type=radio name=restrictresultsview value="n" checked> No
            <input type=radio name=restrictresultsview value="y"> Yes
            <br> Set an expiry date:- <input type=radio name=expires value="n" checked> No
            <input type=radio name=expires value="y"> Yes
            <br> Support user comments?:- <input type=radio name=supportusercomment value="n" checked> No
            <input type=radio name=supportusercomment value="y"> Yes
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
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            surveyname =cgi.escape(self.request.get('surveyname'))

            rtvote=cgi.escape(self.request.get('restrictvote'))
            rtresultsview=cgi.escape(self.request.get('restrictresultsview'))
            
            dbsurveys = db.GqlQuery("SELECT * "
                            "FROM SurveyList ")
            
            for cntr in dbsurveys:
              if cntr.name == surveyname:
                self.response.out.write("<h3>That Survey name --> <b>'%s'</b> is already used please some other survey name.</h3>" % surveyname)
                self.response.out.write("<FORM><INPUT TYPE='button' VALUE='Back' onClick='history.go(-1);return true;'></FORM>")
                return;
                
            newsurvey=SurveyList(creator = users.get_current_user(),name=surveyname,restrictvote=rtvote,restrictresultsview=rtresultsview)
            if newsurvey.name!="":
                newsurvey.put()
            #self.response.out.write("Done")
            
            self.response.out.write('Creating Survey:- ')
            self.response.out.write("""<br>""")
            self.response.out.write(cgi.escape(self.request.get('surveyname')))
            
            erroroccured=0
            if not cgi.escape(self.request.get('noofques')):
                #noofques = int(cgi.escape(self.request.get('noofques')))
            
                self.response.out.write("""<br>No. of questions can't be blank.""")
                erroroccured=1
            if not self.request.get('noofoptionsperques'):
                #noofoptions = int(cgi.escape(self.request.get('noofoptionsperques')))
            
                self.response.out.write("""<br>No. of options per question can't be blank.""")
                erroroccured=1
            if erroroccured==1:
              self.response.out.write("<FORM><INPUT TYPE='button' VALUE='Back' onClick='history.go(-1);return true;'></FORM><br>")
              return
            erroroccured1=0
            try:
                noofques = int(cgi.escape(self.request.get('noofques')))
            except ValueError:
                self.response.out.write("""<br>No. of questions has to be a integer.""")
                erroroccured1=1
            try:
                noofoptions = int(cgi.escape(self.request.get('noofoptionsperques')))
            except ValueError:
                self.response.out.write("""<br>No. of options per question has to be a integer.""")
                erroroccured1=1
            if erroroccured1==1:
              self.response.out.write("<FORM><INPUT TYPE='button' VALUE='Back' onClick='history.go(-1);return true;'></FORM><br>")
              return

            #self.response.out.write("No. of options is %s" % noofoptions)
            useimages = cgi.escape(self.request.get('useimages'))
            useimages="n"
            expires = cgi.escape(self.request.get('expires'))
            supportusrcmmnt=cgi.escape(self.request.get('supportusercomment'))
            
            
            self.response.out.write("""<form name=createform2 action="/create3" enctype="multipart/form-data" method="post">""")
            #if noofques==6:
             # self.response.out.write(range(noofques))
            #else:
             # self.response.out.write("Hey"+noofques)
            self.response.out.write("""<input type=hidden name=expireshidden value=%s>""" % expires)
            if expires=="y":
              self.response.out.write("""<br>Enter number of days and hours till expiry of survey:- 
              <table border="0" cellspacing="0" >
              <tr>
              </td><td align=left> 
              Days<select name='day'>
              <option value='01'>01</option>
              <option value='02'>02</option>
              <option value='03'>03</option>
              <option value='04'>04</option>
              <option value='05'>05</option>
              <option value='06'>06</option>
              <option value='07'>07</option>
              <option value='08'>08</option>
              <option value='09'>09</option>
              <option value='10'>10</option>
              <option value='11'>11</option>
              <option value='12'>12</option>
              <option value='13'>13</option>
              <option value='14'>14</option>
              <option value='15'>15</option>
              <option value='16'>16</option>
              <option value='17'>17</option>
              <option value='18'>18</option>
              <option value='19'>19</option>
              <option value='20'>20</option>
              <option value='21'>21</option>
              <option value='22'>22</option>
              <option value='23'>23</option>
              <option value='24'>24</option>
              <option value='25'>25</option>
              <option value='26'>26</option>
              <option value='27'>27</option>
              <option value='28'>28</option>
              <option value='29'>29</option>
              <option value='30'>30</option>
              <option value='31'>31</option>
              </select>


              </td><td align=left>
              Hours<select name='hours'>
              <option value='00'>00</option>
              <option value='01'>01</option>
              <option value='02'>02</option>
              <option value='03'>03</option>
              <option value='04'>04</option>
              <option value='05'>05</option>
              <option value='06'>06</option>
              <option value='07'>07</option>
              <option value='08'>08</option>
              <option value='09'>09</option>
              <option value='10'>10</option>
              <option value='11'>11</option>
              <option value='12'>12</option>
              <option value='13'>13</option>
              <option value='14'>14</option>
              <option value='15'>15</option>
              <option value='16'>16</option>
              <option value='17'>17</option>
              <option value='18'>18</option>
              <option value='19'>19</option>
              <option value='20'>20</option>
              <option value='21'>21</option>
              <option value='22'>22</option>
              <option value='23'>23</option>
              </select>
              </td></table>""")
            #self.response.out.write("<h5> For those options where you are going to use images, don't write anything in the textbox AND upload the file using 'Choose file' option.</h5>")
            for quesno in range(1,noofques+1):
              self.response.out.write("""Question %s:- <input type=text name=question%s><br>""" % (quesno,quesno))
              if supportusrcmmnt=="y":
                    self.response.out.write("<div style='float:right'>User can enter comment for each question.</style></div>")
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
            self.response.out.write("""<input type=hidden name=supportusercommenthidden value=%s>""" % supportusrcmmnt)
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
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write('Creating Survey:- ')
            surveyname=cgi.escape(self.request.get('surveynamehidden'))
            supportusrcmmnt=cgi.escape(self.request.get('supportusercommenthidden'))
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
            expires=cgi.escape(self.request.get('expireshidden'))
            if expires=="y":
                currentsurvey = db.GqlQuery("SELECT * "
                                "FROM SurveyList "
                                 "WHERE name=:1", surveyname)
                #year=int(cgi.escape(self.request.get('year')))
                #month=int(cgi.escape(self.request.get('month')))
                day1=int(cgi.escape(self.request.get('day')))
                hours1=int(cgi.escape(self.request.get('hours')))
                for cntr6 in currentsurvey:
                    cntr6.expirydate=cntr6.date+datetime.timedelta(days=day1, hours=hours1)
                    cntr6.put()
                
            #self.response.out.write("<br>Hi %sabc" % useimages)
            for cntr in range(1,noofques+1):
              currentquesno="question" + str(cntr)
              if supportusrcmmnt=="n":
                  surveyquestion=Survey(question=cgi.escape(self.request.get(currentquesno)),surveyid=surveyname,usercomment=supportusrcmmnt)
              elif supportusrcmmnt=="y":
                  #currentcmmntno="usrcmmntq" + str(cntr)
                  #usrcmmnt=cgi.escape(self.request.get(currentcmmntno))
                  surveyquestion=Survey(question=cgi.escape(self.request.get(currentquesno)),surveyid=surveyname,usercomment=supportusrcmmnt)
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
                surveyquestion.supportusercomment=db.StringProperty(supportusrcmmnt)
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
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            currentdatetime=datetime.datetime.now()
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList ")

            self.response.out.write("<center>Please select from one of the following surveys:-")
            #self.response.out.write("<form name=voteform1 action='/voteform2'>")
            for cntr in surveylist:
              if cntr.expirydate:
                if cntr.expirydate>currentdatetime:
                  if cntr.restrictvote=="y":
                    friendsofsurveycreator=db.GqlQuery("SELECT * "
                                                       "FROM Friends "
                                                       "WHERE user1=:1",cntr.creator.nickname())
                    for qwe1 in friendsofsurveycreator:
                        for qwe in qwe1.friends:
                          if qwe==user.nickname() or user.nickname()==cntr.creator.nickname():
                              self.response.out.write("<br><a href='/vote2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
                              break
                  if cntr.restrictvote=="n":
                    self.response.out.write("<br><a href='/vote2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
              if not cntr.expirydate:
                if cntr.restrictvote and cntr.restrictvote=="y":
                    friendsofsurveycreator=db.GqlQuery("SELECT * "
                                                       "FROM Friends "
                                                       "WHERE user1=:1",cntr.creator.nickname())
                    for qwe1 in friendsofsurveycreator:
                        for qwe in qwe1.friends:
                          if qwe==user.nickname() or user.nickname()==cntr.creator.nickname():
                              self.response.out.write("<br><a href='/vote2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
                              break
                if cntr.restrictvote and cntr.restrictvote=="n":
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
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            surveyname1 = self.request.get('surveyname')
            self.response.out.write("Voting on survey:- %s" % surveyname1)
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
                
              if cntr1.usercomment and cntr1.usercomment=="y":
                  try:
                      if voteiter.usrcomment!="":
                          self.response.out.write("<br>Write your comments about this question here:- <input type=text name=usrcmmntq%s value=%s><br>" % (j,voteiter.usrcomment))
                  except:
                      self.response.out.write("<br>Write your comments about this question here:- <input type=text name=usrcmmntq%s><br>" % j)
              j+=1
              
            #self.response.out.write("<input type=hidden name=hiddennoofques value=%s>" % count(questionlist))
            self.response.out.write("<input type=hidden name=hiddensurveyname value=%s>" % surveyname1)
            self.response.out.write("<br><input type=submit value='Vote'><input type='reset' value='Clear Form'>")                
            self.response.out.write("</form>")
            self.response.out.write("<br><br>PS:- I will email you your votes.")
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Vote3(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
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
            tomail=""
            tomail+="%s \n \n" % (surveyname1)
            for crntques in questionlist:
                duplicatevote=0
                currentvote=Votes(voter=user, surveyid=surveyname1, question=crntques.question)
                cmnt="usrcmmntq"+str(j)
                currentvote.usrcomment=cgi.escape(self.request.get(cmnt))
                oq="oq"+str(j)
                currentvote.chosenoption=cgi.escape(self.request.get(oq))
                oldquery=db.GqlQuery("SELECT * "
                                     "FROM Votes "
                                     "WHERE surveyid=:1 AND voter=:2 AND question=:3 AND chosenoption=:4 ", surveyname1, user, crntques.question, self.request.get(oq))
                duplicateoccurever=0
                for count9 in oldquery:
                  if currentvote.chosenoption != "" and currentvote.surveyid==count9.surveyid and currentvote.voter==count9.voter and currentvote.question==count9.question and currentvote.chosenoption==count9.chosenoption:
                      if duplicateoccuredever==0:
                          self.response.out.write("<center><h3> If you changed your vote then it has gone through. But I have detected that you are trying to vote multiple times for the same option.  I'm sorry, %s. I'm afraid I can't let you do this.<br> <br>So those votes I won't count again.</h3>" % user.nickname())
                          self. response.out.write("These questions you tried to vote the same option multiple times.")
                      self.response.out.write("<br> %s"% currentvote.question)
                      duplicatevote=1
                      duplicateoccuredever=1
                      
                if currentvote.chosenoption != "" and duplicatevote == 0:
                    oldquery2=db.GqlQuery("SELECT * "
                                     "FROM Votes "
                                     "WHERE surveyid=:1 AND voter=:2 AND question=:3 ", surveyname1, user, crntques.question)
                    for cntr9 in oldquery2:
                      db.delete(cntr9)
                    tomail+="Q:- %s \nA:- %s \n%s \n" % (currentvote.question,currentvote.chosenoption,currentvote.usrcomment)
                    currentvote.put()
                j=j+1
                
            if duplicateoccuredever==1:
                  self.response.out.write("<h3>Click the button to go back.</a>")
                  self.response.out.write("<FORM><INPUT TYPE='button' VALUE='Back' onClick='history.go(-1);return true;'></FORM></center>")
                  return
            self.response.out.write("<br>Voting done. Your votes have been emailed to you. <br><a href='/'> Click here to go to main menu.</a>")
            mail.send_mail(sender="pt795@nyu.edu",
                                   to=user.nickname(),
                                   subject="Your survey votes",
                                   body="""Dear User, Here are your votes for survey:- %s""" % tomail)
            
            
            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Result1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList")
            self.response.out.write("<h2>Viewing Results</h2>")
            self.response.out.write("<h3><div style='float:right'><a href='/popularityresult1'>Arrange Surveys by Popularity. (by votes being cast weighted towards more recent events) </style></div></h3><br><br>")
            self.response.out.write("<center>Please select from one of the following surveys:-")
            #self.response.out.write("<form name=voteform1 action='/voteform2'>")
            for cntr in surveylist:
              if cntr and cntr.restrictresultsview and cntr.restrictresultsview=="y":
                    friendsofsurveycreator=db.GqlQuery("SELECT * "
                                                       "FROM Friends "
                                                       "WHERE user1=:1",cntr.creator.nickname())
                    for qwe1 in friendsofsurveycreator:
                        for qwe in qwe1.friends:
                          if qwe==user.nickname() or user.nickname()==cntr.creator.nickname():
                              self.response.out.write("<br><a href='/result2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
                              break
              if cntr and cntr.restrictresultsview and cntr.restrictresultsview=="n":
                    self.response.out.write("<br><a href='/result2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
                    
                    
              
            self.response.out.write("</center>")            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class PopularityResult1(webapp2.RequestHandler):    
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList")
            self.response.out.write("<h2>Viewing Results <u><i>by Popularity</i></u></h2>")
            self.response.out.write("<center>Please select from one of the following surveys:-")
            #self.response.out.write("<form name=voteform1 action='/voteform2'>")
            
            popularitysurveys={}
            sortpopularitysurveys={}
            
            for cntr in surveylist:
              if cntr and cntr.restrictresultsview and cntr.restrictresultsview=="y":
                    friendsofsurveycreator=db.GqlQuery("SELECT * "
                                                       "FROM Friends "
                                                       "WHERE user1=:1",cntr.creator.nickname())
                    for qwe1 in friendsofsurveycreator:
                        for qwe in qwe1.friends:
                          if qwe==user.nickname() or user.nickname()==cntr.creator.nickname():
                              #self.response.out.write("<br><a href='/result2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
                              popularitysurveys[cntr.name]=0.0
                              break
              if cntr and cntr.restrictresultsview and cntr.restrictresultsview=="n":
                    #self.response.out.write("<br><a href='/result2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
                    popularitysurveys[cntr.name]=0.0
              
            
            dbsurveys = db.GqlQuery("SELECT * "
                            "FROM SurveyList ")
                 
            for cntr1 in dbsurveys:
              votes = db.GqlQuery("SELECT * "
                                   "FROM Votes "
                                   "WHERE surveyid=:1",cntr1.name)
              
              #survey = db.GqlQuery("SELECT * "
              #              "FROM Survey "
              #              "WHERE surveyid=:1", cntr1.name)
              for cntr2 in votes:
                #self.response.out.write(cntr2.surveyid)
                #if (searchcount["%s" % str(cntr2.surveyid)]==null):
                    #searchcount["%s" % str(cntr2.surveyid)]=0
                """date_time1=datetime.datetime.now()
                date_time2 = date_time1.isoformat().split('.')[0].replace('T',' ')
                pattern = '%Y-%m-%d %H:%M:%S'
                sss_s_epoc1 = int(time.mktime(time.strptime(date_time2, pattern)))
                
                date_time4=cntr2.date
                date_time3 = date_time4.isoformat().split('.')[0].replace('T',' ')
                pattern = '%Y-%m-%d %H:%M:%S'
                sss_s_epoc2 = int(time.mktime(time.strptime(date_time3, pattern)))"""
                popularitysurveys[cntr1.name]+=float(1/(float((datetime.datetime.now()-cntr2.date).total_seconds())))
                #searchcount[cntr2.surveyid]+=cntr2.question.count(searchword)
                #for abcd in cntr2.options:
                #   searchcount[cntr2.surveyid]+=abcd.count(searchword)
            self.response.out.write("<center>")
            #for srchcntr in searchercount:
            #found=0
            for key, value in sorted(popularitysurveys.iteritems(), key=lambda (k,v): (v,k)):
                sortpopularitysurveys[key]=value
                #if (value > 0):
                 #   self.response.out.write("<br> %s is %s" % (key, value))
            for k, v in sortpopularitysurveys.iteritems():
                #if (v != 0):
                   self.response.out.write("<br><a href='/result2?surveyname=%s'> %s </a>" % (k, k))
                   #found=1
            #if found==0:
            #  self.response.out.write("<h2>No search results found. Search for some other term using the search box above.</h2>")  
            
                    
              
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
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
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
              oncecommentshown=0
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
                
              for crntvote1 in votelist:
                  if crntvote1.question==ques.question:
                    if crntvote1.usrcomment:
                        if oncecommentshown==0:
                            self.response.out.write("<br><br>User comments for this question are:- ")
                            oncecommentshown=1
                        self.response.out.write("<br>%s" % crntvote1.usrcomment)
              
            
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
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList "
                                "WHERE creator=:1 ", user)
            self.response.out.write("<h2>Selecting Survey to edit.</h2>")
            self.response.out.write("<center>Please select from one of the following surveys created by you:-")
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
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
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
            noofoptions=0
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
            self.response.out.write('To delete a question just make the question text as blank.')
            self.response.out.write(cgi.escape(self.request.get('surveyname')))
            #noofques = int(cgi.escape(self.request.get('noofques')))
            #noofoptions = int(cgi.escape(self.request.get('noofoptionsperques')))
            #useimages = cgi.escape(self.request.get('useimages'))
            if noofques==0:
              self.response.out.write("""<h2>There were no questions found for this survey. go to create a new survey and create a new one and this time do add some questions please!</h2>""")
              
            
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
            self.response.out.write("""<br><br><input type="submit" value="Modify Survey">""")
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
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
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
                  if surveyquestion.question!="":
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
                if surveyquestion.question!="":
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

class AdminEdit1(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! I know you are a <h3>ADMINISTRATOR</h3> (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            surveylist = db.GqlQuery("SELECT * "
                                "FROM SurveyList ")
            self.response.out.write("<h2>Selecting Survey to edit.</h2>")
            self.response.out.write("<center>Please select from one of the following surveys :-")
            #self.response.out.write("<form name=voteform1 action='/voteform2'>")
            for cntr in surveylist:
              self.response.out.write("<br><a href='/edit2?surveyname=%s'> %s </a>" % (cntr.name,cntr.name))
            self.response.out.write("</center>")            
            self.response.out.write("</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Search1(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("<html><body>%s" % greeting)
            self.response.out.write("""<div style="float:right"><a href='/'> Main page </a> | <a href='/create1'> Create survey </a> | <a href='/edit1'> Edit Survey </a> | <a href='/vote'> Vote on survey </a> |  <a href='/result1'> Result </a></style></div>""")
            self.response.out.write("""<br><br><br><br><br><br>""")
            self.response.out.write("""<form name='searchform' action='/search1' method='POST'><div align=right><h3>Search again for a survey:- <br><input type='text' name='searchword'><br><input type='submit' value='Search'> </h3></div></form>""")
            self.response.out.write("<h2>Search results:- </h2><br>")
            searchword=cgi.escape(self.request.get('searchword'))
            dbsurveys = db.GqlQuery("SELECT * "
                            "FROM SurveyList ")
            searchcount = {}
            sortsearchcount = {}

            for cntr1 in dbsurveys:
              survey9 = db.GqlQuery("SELECT * "
                            "FROM Survey "
                            "WHERE surveyid=:1", cntr1.name)
              for cntr2 in survey9:
                #self.response.out.write(cntr2.surveyid)
                #if (searchcount["%s" % str(cntr2.surveyid)]==null):
                  searchcount[cntr2.surveyid]=0
                    
            for cntr1 in dbsurveys:
              searchcount[cntr1.name]+=cntr1.name.count(searchword)
              survey = db.GqlQuery("SELECT * "
                            "FROM Survey "
                            "WHERE surveyid=:1", cntr1.name)
              for cntr2 in survey:
                #self.response.out.write(cntr2.surveyid)
                #if (searchcount["%s" % str(cntr2.surveyid)]==null):
                    #searchcount["%s" % str(cntr2.surveyid)]=0
                searchcount[cntr2.surveyid]+=cntr2.question.count(searchword)
                for abcd in cntr2.options:
                    searchcount[cntr2.surveyid]+=abcd.count(searchword)
            self.response.out.write("<center>")
            #for srchcntr in searchercount:
            found=0
            for key, value in sorted(searchcount.iteritems(), key=lambda (k,v): (v,k)):
                sortsearchcount[key]=value
                #if (value > 0):
                 #   self.response.out.write("<br> %s is %s" % (key, value))
            for k, v in sortsearchcount.iteritems():
                if (v != 0):
                   self.response.out.write("<br><a href='/vote2?surveyname=%s'>%s</a> has your search word:- %s occuring %s times." % (k, k, searchword, v))
                   found=1
            if found==0:
              self.response.out.write("<h2>No search results found. Search for some other term using the search box above.</h2>")
            
            self.response.out.write("</center></body></html>")
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
                               ('/popularityresult1', PopularityResult1),
                               ('/result2',Result2),
                               ('/edit1',Edit1),
                               ('/edit2',Edit2),
                               ('/edit3',Edit3),
                               ('/adminedit1',AdminEdit1),
                               ('/search1', Search1),
                               ('/friend1', Friend1),
                               ('/addfriend1', AddFriend1),
                               ('/addfriend2', AddFriend2)],
                              debug=True)
