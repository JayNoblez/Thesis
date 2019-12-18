#!/usr/bin/python3

import socket
import ssl
import pprint

listen_address = '212.201.8.88'
listen_port = 8083
server_cert = '/home/john/server.crt'
server_key = '/home/john/server.key'
ca_cert = '/home/john/client.crt'

context = ssl.create_default_context()
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=ca_cert)
context.check_hostname = False

sock = socket.socket() 
sock.bind(("", listen_port))
sock.listen(5)

while True:
    new_socket, address = sock.accept()
    print('Connection from: ' + str(address))
    conn = context.wrap_socket(new_socket, server_side=True, server_hostname=None)
    # with context.wrap_socket(new_socket, server_side=True) as ssock:
    pprint.pprint("SSL established. Peer: {}".format(conn.getpeercert()))
    buf = b''  # Buffer to hold received client data
    data = conn.recv(4096).decode()
    if not data:
        break
    else:
        #buf += data # No more data from client. Show buffer and close connection.
        print("Received from user:", data)
        data = input('-> ')
        conn.send(data.encode())
print("Closing Connection")
conn.shutdown(socket.SHUT_RDWR)
conn.close()

