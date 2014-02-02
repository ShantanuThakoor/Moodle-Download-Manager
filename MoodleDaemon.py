#!/usr/bin/python
from gi.repository import Notify
from moodle import *
import os
def mainD():
	if not os.path.exists("daemon.txt"):
		return
	courses=[]
	i=open("daemon.txt")
	arr=i.readlines()
	##print arr
	username=arr[0].strip("\n")
	password=arr[1].strip("\n")
	path=arr[2].strip("\n")
	for n in range(4,len(arr)):
		courses.append(arr[n].strip("\n"))
	mb=MoodleBrowser(username, password, False, path)
	mb.login()
	data={"output":courses}
	##print courses
	mb.downloadCourse(data)
	for f in mb.filesDownloaded:
		Notify.init("c")
		fileDownloaded=Notify.Notification.new("File Downloaded",f,"c")
		fileDownloaded.show ()
		
		#fileDownloaded.hide()

mainD()
