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

    gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

    gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
    #
    # gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
    # gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
    # gmap.heatmap(heat_lats, heat_lngs)
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