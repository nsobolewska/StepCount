from kivy.app import App #for the main app
from kivy.uix.gridlayout import *
from kivy.uix.floatlayout import FloatLayout #the UI layout
from kivy.uix.label import Label #a label to show information
from kivy.uix.button import Button #a label to show information
from plyer import accelerometer #object to read the accelerometer
from kivy.clock import Clock #clock to schedule a method
import sys

class UI(FloatLayout):#the app ui
	tekst = ""
	clic = 0
	def __init__(self, **kwargs):
		super(UI, self).__init__(**kwargs)
		layout = GridLayout(cols=1,rows=3, row_force_default=True, row_default_height=50)
		self.lblAcce = Label(text="Accelerometer: ",width=100,height=20) #create a label at the center
		self.btn = Button(text="Zapisz", width=50,height=50)
		self.btn.bind(on_press=self.save)
		self.btn2 = Button(text="Zakoncz", width=50,height=50)
		self.btn2.bind(on_press=self.koncz)
		layout.add_widget(self.btn)
		layout.add_widget(self.btn2)
		layout.add_widget(self.lblAcce)
		self.add_widget(layout)
		self.tryos()

	def koncz(self,value):
		sys.exit()

	def save(self,instance):
		file2write = open("filename.txt", 'w')
		print("To jest tekst",self.tekst)
		self.tekst = self.tekst+"Koniec"
		file2write.write(self.tekst)
		file2write.close()

	def tryos(self):
		if self.clic == 0:
			try:
				accelerometer.enable() #enable the accelerometer
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
			self.tekst = self.tekst + "X = %.2f	Y = %.2f	Z = %2.f\n"%(
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