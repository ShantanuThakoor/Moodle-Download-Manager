#!usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk
import os
class Base2:
	a={}	

	def combo_text(self, widget):
		#self.textbook.set_text(widget.get_active_text())
		
		if not widget.get_active_text()	in self.a["output"]:		
			self.a["output"].append(widget.get_active_text())
			self.textbuffer.insert_at_cursor(widget.get_active_text())
			self.textbuffer.insert_at_cursor("\n")

	def destroy(self,widget, data=None):
		print "Thank You"
		gtk.main_quit()

	def proceed(self,widget):
		if len(self.a["output"])==0 or self.a["path"]=="":
			err=gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Please Specify Filename and Course")													
			err.run()
			err.destroy()	#to print error message
		else:
			 gtk.main_quit()
			
	
	def browse(self, widget):

		dialog = gtk.FileChooserDialog("Open...", None,
		gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
		(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
		gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		dialog.add_filter(filter)
	
		response=dialog.run()
		if response == gtk.RESPONSE_OK:
			print dialog.get_filename()
			self.textbuffer2.set_text(dialog.get_filename())
			self.a["path"]=dialog.get_filename()
			dialog.destroy()

		elif response == gtk.RESPONSE_CANCEL:
			dialog.destroy()

	def toggle_save(self, widget):
		self.a["check"]=not self.a["check"]

	def __init__(self,d):

		
		
		self.a=d
		
		if os.path.exists("settings.txt"):
			settings = open("settings.txt","r")
			arr=settings.readlines()
			self.a["username"]=arr[0].strip("\n").strip(" ")
			self.a["password"]=arr[1].strip("\n").strip(" ")
			if len(arr)==3:
				self.a["path"]=arr[2].strip("\n").strip(" ")				
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(650,300)
		self.window.set_title("MoodleSync By DeathMegatron2000")
							
		self.button1 = gtk.Button("Submit")
		self.button1.connect("clicked", self.proceed)

		self.button2 = gtk.Button("Browse")
		self.button2.connect("clicked", self.browse)
		
		if os.path.exists("settings.txt"):
			settings=open("settings.txt")
			arr=settings.readlines()
			if len(arr)==3:
				self.a["path"]=arr[2]		

		else:
			self.a["path"]=""

		
	
		self.checker=gtk.CheckButton("Save path")
		self.checker.connect("toggled", self.toggle_save)
		self.checker.set_active(True)
		self.checker.show()		
		
		self.label1 = gtk.Label(" Select Destination Folder ")
		self.label2 = gtk.Label(" Choose your Courses (Upto 7) ")
		self.label3 = gtk.Label(("Welcome Back " + self.a["name"]))
		
		self.textview=gtk.TextView()
		self.textbuffer=self.textview.get_buffer()
		self.textview.show()
		
		self.textview2=gtk.TextView()
		self.textbuffer2=self.textview2.get_buffer()
		m="Default path:\n"+self.a["path"]
		if(self.a["path"]==""):
			m=""
		self.textbuffer2.set_text(m)	
		#self.textbuffer2.set_editable(False)
		self.textview2.show() 

		self.combo=gtk.combo_box_entry_new_text()
		self.combo.connect("changed", self.combo_text)
		for x in range (0,len(self.a["courses"])):
			self.combo.append_text(self.a["courses"][x])
				
		fixed=gtk.Fixed()
		fixed.put(self.label1,90,50)
		fixed.put(self.label2,400,50)
		fixed.put(self.button1,280,200)
		fixed.put(self.button2,140,75)
		fixed.put(self.combo,400,75)
		fixed.put(self.label3,250,25)
		fixed.put(self.textview,400,125)
		fixed.put(self.textview2,90,125)

						#to display all the buttons
		fixed.put(self.checker,90,180)
		self.window.add(fixed)
		self.window.show_all()
		self.window.connect("destroy", self.destroy)
		
	def main(self):
		gtk.main()


'''courseList=["MA 106", "CS 101", "BB 101", "CE 102", "MM 152", "ME 102", "EE 112"]
name = "Shantanu"
output=[]
a={"Courses":courseList,"Name":name,"output":output, "path":"", "check":False}
base=Base2(a)
base.main()
a=base.a
print a'''
