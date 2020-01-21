# TLS_Security_Implementation_Scenarios

This part of the project contains example scripts to test security implementations with IoT Modules. 

For example: For example, to follow with connecting a pycom GPy module over TLSv1.2, please kindly read the following use instructions carefully:

The ClientCode is written in Micropython. To connect to/ upload files to the Gpy module, it is required to have the Atom Pymakr Package installed and configured to the right serial port.  
At the repl prompt, verify that the files are properly uploaded. (import os, os.lisdir('/flash'))

main.py from this repository runs client side socket code on the pycom module, and connect to a remotely listening Whitelisted server at (212.201.8.88, 8083) #IP Address, port of server in the Vodafone backend.
It also passes X509 certificates to the SSL socket. 
connect_nb.py initiates the connection from the pycom module to the vodafone network.

The certificates can be placed in the flash directory - can be passed into the pycom module over FTP or ampy. Again, use os.listdir("/flash/certs") to verify that the certs are correctly placed in the flash directory path as it would not work otherwise.

######
Server code is a typical TCP server, implementing the normal python socket API socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Usage: SSH into server and run remote server to listen for incoming connections from the devices that would want to communicate.
The Certificate chain pre-generated with openSSL is contained in the code, verified on connect. 
