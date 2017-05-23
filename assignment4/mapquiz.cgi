#!/usr/bin/python

import random
import csv
import cgi
import cgitb

class SubwayQuiz:
  def __init__(self, stations_file ):
    self.stations_file = stations_file
  
  def run(self):
    self.openFile()
    self.countSubway()
    self.generateQuiz()
    self.generateHTML()
  
  #open and read in data
  def openFile(self):
    f = open(self.stations_file)
    try:
      reader = csv.reader(f,delimiter=',')
      my_list = list(reader)
    finally:
      f.close()
    self.first,self.rest = my_list[0],my_list[1:]

  #record all distinct subway lines
  def countSubway(self):
    self.subway = set()
    for index in range(0,len(self.rest)):
      for pos in range(5,16):
        if self.rest[index][pos]:
          self.subway.add(self.rest[index][pos])

  #generate choices and answers of the quiz
  def generateQuiz(self):
    self.random_line = random.sample(self.rest,5)
    self.answer = []
    self.choices = []
    for index in range(0,5):
      hold = self.subway.copy()
      valid = []
      for indexOfLine in range(5,16):
        if self.random_line[index][indexOfLine]:
          valid.append(self.random_line[index][indexOfLine])
          hold.remove(self.random_line[index][indexOfLine]) 
      self.answer.append(random.sample(valid,1)[0])
      choice_list = random.sample(hold,3)
      choice_list.append(self.answer[index])
      random.shuffle(choice_list)
      self.choices.append(choice_list)  

  #generate HTML
  def generateHTML(self):
    print "Content-type:text/html"
    print
    print "<html>"
    print "<body>"
    print "<h1>MTA Subway Quiz</h1>"
    self.generateHTMLQuestions()
    print
    print "</body>"
    print "</html>"

  #Generate each questions
  def generateHTMLQuestions(self):
    print "<form>"
    c = 0.0011
    for index in range(0,5):
      print "<p>Question %d:</p>" % (index+1)
      print "<p>Which line stops at <b>%s</b>?</p>" % self.random_line[index][2]
      print "<iframe width=\"425\" height=\"350\" frameborder=\"0\" scrolling=\"no\" marginheight=\"0\" marginwidth=\"0\" src=\"http://www.openstreetmap.org/export/embed.html?bbox=%f,%f,%f,%f&layer=hot&marker=%s,%s\" style=\"border: 1px solid black\"></iframe>" % (float(self.random_line[index][4])-c,float(self.random_line[index][3])-c,float(self.random_line[index][4])+c,float(self.random_line[index][3])+c,self.random_line[index][3],self.random_line[index][4])
      print "<p>"
      for choiceIndex in range(0,4):
        print "<input type=\"radio\" name=\"q%d\" value=\"%s\"> %s<br>" % ((index+1),self.choices[index][choiceIndex],self.choices[index][choiceIndex])
      print "<input type=\"hidden\" name=\"s%d\" value=\"%s\">" % ((index+1),self.random_line[index][2])
      print "<input type=\"hidden\" name=\"a%d\" value=\"%s\">" % ((index+1),self.answer[index])
      print
      print "<hr>"
    print "<input type=\"submit\" value=\"Submit\">"
    print "</form>"

class Grade:
  def __init__(self,form):
    self.form = form
  
  def run(self):
    self.grade()
    self.generateGradeHTML()

  #count the correct choices and incorrect choices
  def grade(self):
    self.correct = []
    self.incorrect = []
    for index in range(0,5):
      choiceKey = "q"+str(index+1)
      choice = form.getvalue(choiceKey)
      nameKey = "s"+str(index+1)
      name = form.getvalue(nameKey)
      answerKey = "a"+str(index+1)
      answer = form.getvalue(answerKey)
      if choice == answer:
        self.correct.append(name)
      else:
        self.incorrect.append(name)

  def generateGradeHTML(self):
    print "Content-type:text/html"
    print
    print "<html>"
    print "<h2>Your score:%d%%</h2>" % (len(self.correct)*20)
    print "<h3>Correct answers</h3>"
    for index in range(0,len(self.correct)):
      print "<font color=green>%s</font><br>" % self.correct[index]
    print "<h3>Incorrect answers</h3>"
    for index in range(0,len(self.incorrect)):
      print "<font color=red>%s</font><br>" % self.incorrect[index]
    print "</html>"


if __name__ == "__main__":
  cgitb.enable()
  form = cgi.FieldStorage()
  if (form.has_key("a1")):
    result = Grade(form)
    result.run()
  else:
    sub = SubwayQuiz('/home/unixtool/data/mta/StationEntrances.csv')
    sub.run()

