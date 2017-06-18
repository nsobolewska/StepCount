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
	names = 0
	nameOfFileA = "akcelerometr.txt"
	nameOfFileG = "gps.txt"
	file2write = open(nameOfFileA, 'w')
	file2write.write(tekst)
	file2write.close()
	file2write2 = open(nameOfFileG, 'w')
	file2write2.write(tekst2)
	file2write2.close()
	def __init__(self, **kwargs):
		super(UI, self).__init__(**kwargs)
		layout = GridLayout(cols=1,rows=5, row_force_default=True, row_default_height=200)
		self.lblAcce = Label(text="Accelerometer: ",width=100,height=20) #create a label at the center
		self.btn = Button(text="Zapisz", width=50,height=50)
		self.btn.bind(on_press=self.save)
		self.btn2 = Button(text="Zakoncz", width=50,height=50)
		self.btn2.bind(on_press=self.koncz)
		self.btn3 = Button(text="Start akcelerometr", width=50,height=50)
		self.btn3.bind(on_press=self.tryos)
		self.btn4 = Button(text="Start gps", width=50,height=50)
		self.btn4.bind(on_press=self.gpstart)
		layout.add_widget(self.btn)
		layout.add_widget(self.btn2)
		layout.add_widget(self.btn3)
		layout.add_widget(self.btn4)
		layout.add_widget(self.lblAcce)
		self.add_widget(layout)
		# self.tryos()
		Clock.schedule_interval(self.save, 180)

	def gpstart(self,instance):
		try:
			gps.configure(on_location=self.print_locations)
			gps.start()
		except:
			self.lblAcce.text = "Failed to start gps"  # error



	def koncz(self,value):
		sys.exit()

	def print_locations(self,**kwargs):
		self.tekst2 = self.tekst2+ '{lat}	{lon}	'.format(**kwargs) #latitude longitude

	def save(self,instance):
		#--------------ZAPISZ DO PLIKU--------------------#
		nameOfFileA = "akcelerometr.txt"
		nameOfFileG = "gps.txt"
		file2write = open(nameOfFileA, 'a')
		file2write.write(self.tekst)
		file2write.close()
		file2write2 = open(nameOfFileG, 'a')
		file2write2.write(self.tekst2)
		file2write2.close()
		self.tekst = ""
		self.tekst2 = ""
		#-------------------------------------------------#
		# #-------------------------------------------------#
		# #-----------SOCKET--------------------------------#
		# host = "192.168.8.100"
		# port = 3000
		# self.s = socket.socket()
		# self.s.connect((host, port))
		# self.tekst = "Koniec" #self.tekst +
		# encoded_msg = bytes(self.tekst, "utf-8")
		# self.s.send(encoded_msg)
		# #-------------------------------------------------#
		# for line in self.tekst:
		# 	self.sock.send(str.encode(line))
		# 	time.sleep(1/20)

	def tryos(self,instance):
		try:
			accelerometer.enable() #enable the accelerometer
			#if you want do disable it, just run: accelerometer.disable()
			Clock.schedule_interval(self.update, 1.0/15) #24 calls per second
		except:
			self.lblAcce.text = "Failed to start accelerometer" #error

	def update(self, dt):
		txt = ""
		try:
			txt = "Accelerometer:\nX = %.2f\nY = %.2f\nZ = %.2f " %(
				accelerometer.acceleration[0], #read the X value
				accelerometer.acceleration[1], # Y
				accelerometer.acceleration[2]) # Z

		except:
			txt = "Cannot read accelerometer!" #error
		try:
			self.tekst = self.tekst + "%.2f	%.2f	%.2f\n"%(		#x,y,z from accelerometer
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