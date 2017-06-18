import socket
import gmplot
import numpy as np
import matplotlib.pyplot as mpl
from scipy import signal
import time
import sys
from PyQt5.QtWidgets import *
# QMainWindow, QPushButton, QApplication, QAction
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, Qt

class Window(QMainWindow):
    tekst = ""
    nameOfFileA = "akcelerometr1.txt"
    nameOfFileG = "gps1.txt"
    file2write = open(nameOfFileA, 'w')
    file2write.write(tekst)
    file2write.close()
    file2write2 = open(nameOfFileG, 'w')
    file2write2.write(tekst)
    file2write2.close()
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(150, 150, 500, 500)
        self.okno = QWidget(self)
        self.setCentralWidget(self.okno)
        self.mainLayout = QVBoxLayout()
        # self.mainLayout.setGeometry(100,100,300,300)
        self.gridLayout = QGridLayout()
        self.okno.setLayout(self.mainLayout)
        self.setWindowTitle("Movemeter")
        self.home()
        self.mainLayout.addLayout(self.gridLayout)
        self.show()
        # buttons
    def home(self):
        self.resultlabel = QLabel("Liczba krokow: ", self)
        self.resultlabel.setFont(QtGui.QFont('SansSerif', 15))
        self.resultlabel.resize(self.resultlabel.minimumSizeHint())
        self.mainLayout.addWidget(self.resultlabel)

        self.btn0 = QPushButton('Licz kroki i wykresl wykresy', self)
        self.btn0.clicked.connect(self.akcelerometr)
        self.btn0.resize(self.btn0.minimumSizeHint())
        self.gridLayout.addWidget(self.btn0, 1, 0)

        self.btn1 = QPushButton('Wykresl trase na mapach google', self)
        self.btn1.clicked.connect(self.googlemap)
        self.btn1.resize(self.btn1.minimumSizeHint())
        self.gridLayout.addWidget(self.btn1, 1, 1)

        self.btn2 = QPushButton('Wlacz serwer', self)
        self.btn2.clicked.connect(self.on_click2)
        self.btn2.resize(self.btn2.minimumSizeHint())
        self.gridLayout.addWidget(self.btn2, 2, 0)

        self.btn3 = QPushButton('Wylacz serwer', self)
        self.btn3.clicked.connect(self.on_click3)
        self.btn3.resize(self.btn3.minimumSizeHint())
        self.gridLayout.addWidget(self.btn3, 2, 1)


        self.btn0.setFixedSize(200, 100)
        self.btn1.setFixedSize(200, 100)
        self.btn2.setFixedSize(200, 100)
        self.btn3.setFixedSize(200, 100)

    def on_click2(self):
        print("Wlaczanie serwera")

    def on_click3(self):
        print("Wylaczanie serwera")

    def akcelerometr(self):
        with open("akcelerometr.txt", "r") as ins:
            akc = []
            for line in ins:
                for word in line.split():
                    akc.append(word)
        akcX = []
        akcY = []
        akcZ = []
        i = 0
        while i < len(akc):
            akcX.append(akc[i])
            akcY.append(akc[i + 1])
            akcZ.append(akc[i + 2])
            i += 3

        Z = np.zeros(len(akcZ))
        for j in range(len(akcZ)):
            Z[j] = float(akcZ[j])
        Z = Z - np.mean(Z)
        time = np.ones(len(akcX))
        time = np.cumsum(time)
        # time = time/24
        mag = np.zeros(len(akcX))
        for j in range(len(akcX)):
            mag[j] = np.sqrt((float)(akcX[j])**2 + (float)(akcY[j])**2 + (float)(akcZ[j])**2)

        magNoG = mag - np.mean(mag)

        minPeakHeight = np.std(magNoG)

        maxPeakHeight = minPeakHeight + 1

        pks = signal.find_peaks_cwt(magNoG,np.arange(1,6))
        # pks = signal.argrelextrema(magNoG, np.greater)
        magNoG2 = 1/magNoG
        pks2 = signal.find_peaks_cwt(magNoG2,np.arange(1,6))


        minPeakHeight2 = np.std(Z)
        print(minPeakHeight2)
        kroki = 0
        kroki2 = 0
        # print(magNoG(pks))
        for loc in pks:
        #     if magNoG[loc]>minPeakHeight and Z[loc]>minPeakHeight2 and magNoG[loc]<maxPeakHeight :
            kroki+=1
        for loc in pks:
        #     if magNoG[loc]>minPeakHeight and Z[loc]>minPeakHeight2 and magNoG[loc]<maxPeakHeight :
            kroki2+=1

        print("Ilosc krokow",kroki)
        print("Ilosc krokow",kroki2)
        mpl.plot(time,akcX,'r')
        mpl.plot(time, akcY, 'g')
        mpl.plot(time, akcZ, 'b')
        mpl.plot(time, magNoG, 'y')

        mpl.show()

    def googlemap(self):
        with open("gps1.txt", "r") as ins:
            gps = []
            for line in ins:
                for word in line.split():
                    gps.append(word)

        latitudes = []
        longitudes = []
        i=0
        while i<len(gps)-1:
            latitudes.append(float(gps[i]))
            longitudes.append(float(gps[i+1]))
            i+=2

        for k in range(1,len(latitudes)-1):
            mod1a = np.abs(latitudes[k]-latitudes[k+1])
            mod1o = np.abs(longitudes[k] - longitudes[k + 1])
            if mod1a>0.0007 or mod1o>0.0007:
                mod2a = np.abs(latitudes[k-1] - latitudes[k])
                mod2o = np.abs(longitudes[k - 1] - longitudes[k])
                if mod2o>0.0007 or mod2a>0.0007:
                    latitudes[k] = latitudes[k-1]
                    longitudes[k] = longitudes[k-1]
                else:
                    latitudes[k+1] = latitudes[k]
                    longitudes[k+1] = longitudes[k]

        gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 16)

        gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
        gmap.draw("mymap2.html")

    def server(self):
        akcele = 0
        gpse = 0
        pierw = 0
        nameOfFileA = "akcelerometr1.txt"
        nameOfFileG = "gps1.txt"
        host = "192.168.8.100"
        port = 3000
        s = socket.socket()
        s.bind((host, port))
        s.listen(10)
        while True:
                c, addr=s.accept()
                print("\nconnection successful with "+str(addr)+"\n\n")
                data = c.recv(1024)
                while data:
                    decoded_data=data.decode("utf-8")
                    if decoded_data=="A":
                        akcele = 1
                        pierw = 1
                        gpse = 0
                    if decoded_data == "G":
                        akcele = 0
                        pierw = 1
                        gpse = 1
                    if decoded_data=="K":
                        akcele = 0
                        gpse = 0
                    if akcele == 1 and pierw == 0:
                        decoded_data = "\n" + decoded_data + " "
                        file2write = open(nameOfFileA, 'a')
                        file2write.write(decoded_data)
                        file2write.close()
                    if gpse == 1 and pierw == 0:
                        decoded_data = "\n" + decoded_data + " "
                        file2write = open(nameOfFileG, 'a')
                        file2write.write(decoded_data)
                        file2write.close()
                    if not decoded_data:
                            print("connection with "+ str(addr)+ " broken\n")
                    else:
                            print("-> "+ decoded_data + "\n")
                    pierw = 0
                    data = c.recv(20)

def run():

    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec())

run()