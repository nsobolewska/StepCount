import socket

host="192.168.8.100"
port=5005
s=socket.socket()
s.bind((host, port))
s.listen(10)

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

server()