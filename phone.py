from kivy.app import App #for the main app
from kivy.uix.gridlayout import *
from kivy.uix.floatlayout import FloatLayout #the UI layout
from kivy.uix.label import Label #a label to show information
from kivy.uix.button import Button #a label to show information
from plyer import accelerometer #object to read the accelerometer
from plyer import gps
from kivy.clock import Clock #clock to schedule a method
import time
import sys
import socket

class UI(FloatLayout):#the app ui
	tekst = ""
	tekst2 = ""
	clic = 0
	def __init__(self, **kwargs):
		super(UI, self).__init__(**kwargs)
		layout = GridLayout(cols=1,rows=4, row_force_default=True, row_default_height=300)
		self.lblAcce = Label(text="Accelerometer: ",width=100,height=20) #create a label at the center
		self.lblAcce2 = Label(text="Gps: ",width=100,height=20) #create a label at the center
		self.btn = Button(text="Zapisz", width=50,height=50)
		self.btn.bind(on_press=self.save)
		self.btn2 = Button(text="Zakoncz", width=50,height=50)
		self.btn2.bind(on_press=self.koncz)
		layout.add_widget(self.btn)
		layout.add_widget(self.btn2)
		layout.add_widget(self.lblAcce)
		layout.add_widget(self.lblAcce2)
		self.add_widget(layout)
		gps.configure(on_location=self.print_locations)
		self.tryos()

	def koncz(self,value):
		sys.exit()

	def print_locations(self,**kwargs):
		self.tekst2 = self.tekst2+ 'lat: {lat}, lon: {lon}'.format(**kwargs)

	def save(self,instance):
		#--------------ZAPISZ DO PLIKU--------------------#
		file2write = open("akcelerometr.txt", 'w')
		file2write.write(self.tekst)
		file2write.close()
		file2write2 = open("gps.txt", 'w')
		file2write2.write(self.tekst2)
		file2write2.close()
		#-------------------------------------------------#
		# #-------------------------------------------------#
		# #-----------SOCKET--------------------------------#
		# host = "192.168.8.100"
		# port = 5005
		# self.s = socket.socket()
		# self.s.connect((host, port))
		# self.tekst = "Koniec" #self.tekst +
		# encoded_msg = bytes(self.tekst, "utf-8")
		# self.s.send(encoded_msg)
		# #-------------------------------------------------#
		# for line in self.tekst:
		# 	self.sock.send(str.encode(line))
		# 	time.sleep(1/20)

	def tryos(self):
		if self.clic == 0:
			try:
				accelerometer.enable() #enable the accelerometer
				gps.start()
				#if you want do disable it, just run: accelerometer.disable()
				Clock.schedule_interval(self.update, 1.0/24) #24 calls per second
			except:
				self.lblAcce.text = "Failed to start accelerometer" #error

	def update(self, dt):
		txt = ""
		try:
			txt = "Accelerometer:\nX = %.2f\nY = %.2f\nZ = %2.f " %(
				accelerometer.acceleration[0], #read the X value
				accelerometer.acceleration[1], # Y
				accelerometer.acceleration[2]) # Z

		except:
			txt = "Cannot read accelerometer!" #error
		try:
			self.tekst = self.tekst + "%.2f	%.2f	%2.f\n"%(		#x,y,z from accelerometer
			accelerometer.acceleration[0], #read the X value
			accelerometer.acceleration[1], # Y
			accelerometer.acceleration[2]) # Z
		except:
			txt = "Cannot read accelerometer!" #error
		self.lblAcce.text = txt #add the correct text

class Accelerometer(App): #our app
	def build(self):
		ui = UI()# create the UI
		return ui #show it

if __name__ == '__main__':

	Accelerometer().run() #start our app