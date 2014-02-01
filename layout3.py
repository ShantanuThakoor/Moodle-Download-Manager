import pygtk
pygtk.require('2.0')
import gtk
import os

class Base3:
	def destroy(self,widget,data=None):
		#print "Thank You."
		gtk.main_quit()

	def perform(self, widget):
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(True)
		self.window.set_title("Welcome to MoodleSync by DeathMegatron2000")
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(450,250)
		self.window.show()
		self.window.connect("destroy",self.destroy)

		self.button1 = gtk.Button("Close")
		self.button1.connect("clicked",self.perform)

		self.error_label = gtk.Label("Incorrect LDAP id or Password")
		
		self.image=gtk.Image()
		self.image.set_from_file("error.png")

		fixed = gtk.Fixed()
		fixed.put(self.button1,250,125)
		fixed.put(self.error_label,200,50)
		fixed.put(self.image,50,50)
		self.window.add(fixed)
		self.window.show_all()

	def main(self):
		gtk.main()


