# main.py -- put your code here!
from network import WLAN
from connect_nb import Connection
import machine
import socket
import ssl
import sys
import time
import uos

#create Connection object:
connection = Connection()

#Connect to the LTE Network
connection.nb_connect()

server_address = socket.getaddrinfo("212.201.8.88", 8082)[0][-1]
client_key = '/flash/cert/client.key'
client_cert = '/flash/cert/client.crt'
ca_crt = '/flash/cert/server.crt'

if connection.lte.isconnected():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a socket (SOCK_STREAM means a TCP socket
    ss = ssl.wrap_socket(sock, keyfile = client_key, certfile = client_cert,server_side=False, cert_reqs=ssl.CERT_REQUIRED,ca_certs=ca_crt, timeout=10000)
    ss.connect(server_address)
    print("Connection to server successful")
    message = input(" -> ")
    while message.lower().strip() != "bye":
        to_send = (message.encode())
        ss.send(to_send)
        data = ss.recv(4096).decode()
        print('Received from server: ' + data)
        message = input(" -> ")
    ss.close()
