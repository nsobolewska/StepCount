import socket
import gmplot
import numpy as np
import matplotlib.pyplot as mpl
from scipy import signal
import time
import googlemaps
from datetime import datetime

# googleapi key: AIzaSyD80pxex1anVGvFuK47zOpN2owAoTyE9HM

host="192.168.8.100"
port=3000
s=socket.socket()
s.bind((host, port))
s.listen(10)

def akcelerometr():
    with open("akcelerometr0.txt", "r") as ins:
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

def googlemap():

    with open("gps.txt", "r") as ins:
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
        i+=1
    print(gps)
    # latitudes = [54.5496054,54.5496054,54.5496912599,54.5496912599]
    # longitudes = [18.5462068,18.5462068,18.5463277236,18.5463277236]

    gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 16)

    gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
    gmap.draw("mymap.html")

def server():
        while True:
                c, addr=s.accept()
                print("\nconnection successful with "+str(addr)+"\n\n")
                data=c.recv(1024)
                decoded_data=data.decode("utf-8")
                if not decoded_data:
                        print("connection with "+ str(addr)+ " broken\n")
                else:
                        print("-> "+ decoded_data + "\n")

# server()
# akcelerometr()
googlemap()