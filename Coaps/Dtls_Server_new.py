import socket
from dtls.wrapper import wrap_server
from os import path

# CoAPthon
from coapthon.server.coap import CoAP as CoAPServer
from exampleresources import Storage
import time

# Logging
from logging import basicConfig, DEBUG, getLogger, root, Filter
basicConfig(level=DEBUG, format="%(asctime)s - %(threadName)-30s - %(name)s - %(levelname)s - %(message)s")
_logger = getLogger(__name__)


def main():
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _sock.settimeout(300)
    cert_path = path.join(path.abspath(path.dirname(__file__)), "certs")
    host_address = ("212.201.8.88", 9999)

    # Set up a server side DTLS socket
    dtls_sock = wrap_server(_sock,
                            keyfile=path.join(cert_path, "keycert.pem"),
                            certfile=path.join(cert_path, "keycert.pem"),
                            ca_certs=path.join(cert_path, "ca-cert.pem"), )
    dtls_sock.bind(host_address)
    dtls_sock.listen(1)
    print ("listening for peer")

    # Connect the Listening DTLS socket to CoAP
    server = CoAPServer(host_address, sock=dtls_sock)
    server.add_resource('storage/', Storage())
    print("CoAP Server start on " + host_address[0] + ":" + str(host_address[1]))
    while True:
        time.sleep(0.5)
        try:
            server.listen(1)
        except KeyboardInterrupt:
            print "Server Shutdown"
            server.close()
            print "Exiting..."


if __name__ == "__main__":
    main()

# To-dos: Improve code style
# Get the IP address of the server from the Command
# Use OOP
# Handle Errors
