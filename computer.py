import socket
import gmplot
import time
import googlemaps
from datetime import datetime

# googleapi key: AIzaSyD80pxex1anVGvFuK47zOpN2owAoTyE9HM

host="192.168.8.100"
port=5005
s=socket.socket()
s.bind((host, port))
s.listen(10)

def googlemap():

    latitudes = [54.5496054,54.5496054,54.5496912599,54.5496912599]
    longitudes = [18.5462068,18.5462068,18.5463277236,18.5463277236]

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
googlemap()