from crontab import CronTab
from bs4 import *
from requests import *
from mechanize import *
import os
from layout1 import *
from layout2 import *
from layout3 import *
class MoodleBrowser:
	path=""
	filesDownloaded=[]
	courseList=[]
	b=""
	defaultUrl="http://moodle.iitb.ac.in/"
	loggedin=False
	username=""
	password=""
	write1=False
	write2=False
	name=""
	
	def __init__(self,u,p,c,pa):
		self.defaultUrl="http://moodle.iitb.ac.in/"
		self.path=pa
		self.username=u
		self.password=p
		self.write1=c
		self.loggedin=False
		self.b=Browser()
		self.b.set_handle_robots(False)
		self.b.open(self.defaultUrl)		
		

	def login(self):
		soup = BeautifulSoup(self.b.response().read())
		firstTitle = soup.title
		#print firstTitle
		self.b.select_form(nr=0)
		self.b.form["username"]=self.username
		self.b.form["password"]=self.password
		self.b.submit()
		print "Logging in!"
		soup=BeautifulSoup(self.b.response().read())
		secondTitle=soup.title
		#print secondTitle
		if(firstTitle==secondTitle):
			print "Unuccessful Login"
			self.loggedin=False

		else:
			print "Login successful"
			self.loggedin=True
		
	def getCourses(self):
		array=[]
		soup = BeautifulSoup(self.b.response().read())
		for link in soup.find_all('a'):
			h=link.get('href')
			if(link.get('title') != "Click to enter this course"):
				continue
		
			if(link.text[0:6] in array):
				continue
		
			array.append(link.text[0:6])
		
		self.courseList=array
	
	def getName(self):
		n=""
		soup = BeautifulSoup(self.b.response().read())
		div=soup.find("div",{"class":"logininfo"})
		n=(div.find("a").text)	
		self.name=n
		

	def writeToFile(self, i=True):
		filename="settings.txt"
		f=open(filename,"w+")
		f.write(self.username+"\n")
		f.write(self.password+"\n")
		if(i):
			f.write(self.path)

		f.close()

	def getCourseUrl(self,course):
		courseUrl=[]
		print course
		soup = BeautifulSoup(self.b.response().read())
		for link in soup.find_all('a'):
			if(link.get('title') != "Click to enter this course"):
				continue
			if(link.text[0:6]!=course):
				continue
			courseUrl.append(link.get('href'))
		return courseUrl
	
	def download(self, lecture, s,name):
		self.b.open(lecture)
		soup = BeautifulSoup(self.b.response().read())
		#print soup.title
		for link in soup.find_all('a'):
			downloadLink=link.get('href')
			k = downloadLink.rfind(".")
			name2=name
			if not "?forcedownload=1" in name:
				name2 = name +"." + downloadLink[k+1:]
			name3 = name2.replace(" File","").replace(" Folder","").replace("?forcedownload=1","").replace("/","  ")
			name3=name3.strip(" ")
			
			if not "plugin" in downloadLink:
				continue
					
			#print downloadLink ,name2
			directory=self.path
			subdir=s
    			p=os.path.join(directory,subdir)
			if not os.path.exists(p):
				os.makedirs(p)			
			if os.path.exists(os.path.join(p,name3)):
				continue
			print name3				
			self.b.retrieve(downloadLink,os.path.join(p,name3))
			self.filesDownloaded.append(os.path.join(p,name3))
		

	def writeDaemon(self, courses, timeChoice):
		out=open("daemon.txt",'w')
		out.write(self.username+"\n")
		out.write(self.password+"\n")
		out.write(self.path+"\n")
		out.write(str(timeChoice)+"\n")
		for course in courses:
			out.write(course)
			out.write("\n")

	def downloadAll(self, url, s):

		#print s
		newUrl=url.encode("ascii","ignore")
		self.b.open(newUrl)
		lectureUrl=[]
		soup = BeautifulSoup(self.b.response().read())
		#print soup.title
		tempList=[]
		namesList=[]
		t1=(soup.find_all("li",{"class":"activity folder modtype_folder"}))
		t2=(soup.find_all("li",{"class":"activity resource modtype_resource"})) 
		tempList=t1+t2
		for element in tempList:
			lectureUrl.append((element.find("a").get('href')))
			namesList.append((element.find('a').text))
			
		#print lectureUrl
		#print namesList
		for i in range(0,len(lectureUrl)):
			self.download(lectureUrl[i].encode("ascii", "ignore"),s,namesList[i])



	def downloadCourse(self, data):
		for course in data["output"]:
			self.b.open("http://moodle.iitb.ac.in")			
			courseUrl=self.getCourseUrl(course)
			print courseUrl
			if len(courseUrl)>0:
				self.downloadAll(courseUrl[0],course)
			if len(courseUrl)==2:
				self.downloadAll(courseUrl[1],course)
	def activateDaemon(self, t):
		cron=CronTab(user=True)
		job=cron.new(command="MoodleDaemon.py")
		if(t==1):
			job.week.every(1)
		if(t==2):
			job.day.every(1)
		if(t==3):
			job.hour.every(1)
		#job.append.every_reboot()
		job.enable()
		
	def deactivateDaemon(self):
		cron=CronTab(user=True)
		
		
		j=cron.find_command("MoodleDaemon.py")
		try:
			cron.remove(job)		
		except:
			j=""
	
def main():
	
	##### data2 and a should be empty dicts for actual app
	a={"username":"", "password":"", "checked":False, "path":"", "error":False}
	#	use GUI to change a
	base1=Base1(a)
	base1.main()
	a=base1.a
	o=[]
	mb=MoodleBrowser(a["username"],a["password"],a["checked"],a["path"])
	mb.login()
	print mb.loggedin
	if not mb.loggedin:
		base3=Base3()
		base3.main()
		return
	mb.getCourses()
	mb.getName()
	if(mb.write1):
		mb.writeToFile()

	data2={"error": "False", "name":mb.name, "check":"False","path":"","courses":mb.courseList, "output":o, "timeChoice":0}
	
	#0: never 1:weekly 2:daily 3:hourly -1:noChange
	#use GUI2 to get data2 and update mb.path
	base2=Base2(data2)
	base2.main()
	data2=base2.a
	#print data2
	mb.path=data2["path"]
	mb.write2=not data2["check"]
	mb.downloadCourse(data2)
	mb.writeToFile(mb.write2)
	if data2["timeChoice"]!=-1:
		mb.writeDaemon(data2["output"],data2["timeChoice"])
	elif data2["timeChoice"]==0:
		mb.deactivateDaemon()
	else:
		mb.deactivateDaemon()
		mb.activateDaemon(data2["timeChoice"])


#main()
