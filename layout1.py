import mechanize
import bs4
import pygtk
pygtk.require("2.0")
import gtk
import os
class Base1:
	#def toggle_save_details(self, checkbutton, textview):
	#save login details
	checkBox=False
	a={}
	def destroy(self,widget,data=None):
		#print "Thank You."
		gtk.main_quit()

	def toggle_save(self,checkbutton):
		self.a["checked"]=not self.a["checked"]

	def user_entered(self,widget):
		1

	def pass_entered(self,widget):
		1

	def proceed_ahead(self,widget):
		self.status = self.checker.get_active()

		if(self.usertext.get_text() == "" or self.passtext.get_text() == ""):
			err = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Empty Username or Password")
			err.run()
			err.destroy()
		else:	
				self.a["username"]=self.usertext.get_text()
	 			self.a["password"]=self.passtext.get_text()
				self.a["checked"]=self.status
				gtk.main_quit()


	def __init__(self,d):
		self.a=d

		if os.path.exists("settings.txt"):
			settings = open("settings.txt","r")
			arr=settings.readlines()
			self.a["username"]=arr[0].strip("\n").strip(" ")
			##print self.a["username"]
			self.a["password"]=arr[1].strip("\n").strip(" ")
			if len(arr)==3:
				self.a["path"]=arr[2].strip("\n").strip(" ")
		else:
			self.a={"username":"", "password":"", "checked":False, "path":"", "error":False}

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(True)
		self.window.set_title("Welcome to MoodleSync by DeathMegatron2000")
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(600,300)
		self.window.show()
		self.window.connect("destroy",self.destroy)
		
		self.button1 = gtk.Button("Submit")
		self.button1.connect("clicked",self.proceed_ahead)

		self.user_label = gtk.Label("Username")
		self.pass_label = gtk.Label("Password")
		self.info_label = gtk.Label("Enter your LDAP id and Password")

		self.usertext = gtk.Entry()
		self.usertext.connect("changed",self.user_entered)
		self.usertext.set_editable(True)
		##print self.a["username"]
 		self.usertext.set_text(self.a["username"])

		self.passtext = gtk.Entry()
		self.passtext.connect("changed",self.pass_entered)
		self.passtext.set_visibility(False)
		self.passtext.set_editable(True)
		self.passtext.set_text(self.a["password"])

		self.image=gtk.Image()
		self.image.set_from_file("moodle.png")

		self.checker = gtk.CheckButton("Save User Details")
		self.checker.connect("toggled", self.toggle_save)
		self.checker.set_active(True)
		self.a["checked"]=not self.a["checked"]
		self.checker.show()
		
		
		fixed = gtk.Fixed()
		fixed.put(self.button1,300,200)
		fixed.put(self.info_label,270,50)
		fixed.put(self.user_label,250,100)
		fixed.put(self.pass_label,250,150)
		fixed.put(self.usertext,350,100)
		fixed.put(self.passtext,350,150)
		fixed.put(self.image,50,50)
		fixed.put(self.checker,400,200)

		self.window.add(fixed)
		self.window.show_all()

	def main(self):
		gtk.main()

'''#if __name__ == "__main__":
a={"username":"", "password":"", "checked":False, "path":""}
base=Base1(a)
base.main()
#print base.a'''
