""" Copy rights 2019, Mahmoud Mansour. FlexQuartier Project - THM"""

from connect_nb import Connection
import socket
import time



#create Connection object:
connection = Connection()

#Connect to the LTE Network
connection.nb_connect()


#proxy configs:
address = "212.201.8.88"
port = 6001

#create a socket:
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#establsih a TCP connection to the white listed server
s.connect((address,port))

count = 0
while count < 3 :
    count += 1
    s.send(b"Hello")
    data = s.recv(1024)
    print(data)
    time.sleep(10)

#GO to sleep
s.close()

print('end of main!')
