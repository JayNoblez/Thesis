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

    server = CoAPServer(host_address, sock=dtls_sock)
    server.add_resource('storage/', Storage())
    print("CoAP Server start on " + host_address[0] + ":" + str(host_address[1]))
    while True:
        # addr = _ssock.listen()
        # Connect the CoAP server to the newly created socket
        time.sleep(0.5)
        try:
            # dtls_sock.listen(1)
            server.listen(1)
        except KeyboardInterrupt:
            print "Server Shutdown"
            server.close()
            print "Exiting..."


if __name__ == "__main__":
    main()

    # cb_ignore_listen_exception=_cb_ignore_listen_exception
    # if addr:
    #     print("Completed listening for peer: {}".format(addr))
    #     print(_ssock)
    #     break
#
# print("Accepting")
# conn = _ssock.accept()[0]
#
# while True:
#     addr = _ssock.listen()
#     assert not addr
#     try:
#         conn.do_handshake()
#     except SSLError as err:
#         if err.errno == 504:
#             continue
#         raise
#     print "Completed handshaking with peer"
#     break
#
# while True:
#     addr = _ssock.listen()
#     assert not addr
#     try:
#         message = conn.read()
#     except SSLError as err:
#         if err.errno == 502:
#             continue
#         if err.args[0] == SSL_ERROR_ZERO_RETURN:
#             break
#         raise
#     print message
#     conn.write("Back to you: " + message)
#
# while True:
#     peer_address = _ssock.listen()
#     assert not peer_address
#     try:
#         s = conn.shutdown()
#         s.shutdown(socket.SHUT_RDWR)
#     except SSLError as err:
#         if err.errno == 502:
#             continue
#         raise
#     break
