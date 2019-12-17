#!/usr/bin/env python
import getopt
import socket
import sys
import ssl
from os import path

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from dtls.wrapper import wrap_client

# Logging
from logging import basicConfig, DEBUG, getLogger, root, Filter

basicConfig(level=DEBUG, format="%(asctime)s - %(threadName)-30s - %(name)s - %(levelname)s - %(message)s")

_logger = getLogger(__name__)
cert_path = path.join(path.abspath(path.dirname(__file__)), "certs")

client = None


def usage():  # pragma: no cover
    print "Command:\tcoapclient.py -o -p [-P] [-u]"
    print "Options:"
    print "\t-o, --operation=\tGET|PUT|POST|DELETE|DISCOVER|OBSERVE"
    print "\t-p, --path=\t\tPath of the request"
    print "\t-P, --payload=\t\tPayload of the request"
    print "\t-f, --payload-file=\tFile with payload of the request"
    print "\t-u, --proxy-uri-header=\tProxy-Uri CoAP Header of the request"


def client_callback(response):
    print "Callback"


def client_callback_observe(response):  # pragma: no cover
    global client
    print "Callback_observe"
    check = True
    while check:
        chosen = raw_input("Stop observing? [y/N]: ")
        if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
            print "Unrecognized choose."
            continue
        elif chosen == "y" or chosen == "Y":
            while True:
                rst = raw_input("Send RST message? [Y/n]: ")
                if rst != "" and not (rst == "n" or rst == "N" or rst == "y" or rst == "Y"):
                    print "Unrecognized choose."
                    continue
                elif rst == "" or rst == "y" or rst == "Y":
                    client.cancel_observing(response, True)
                else:
                    client.cancel_observing(response, False)
                check = False
                break
        else:
            break


def main():  # pragma: no cover
    global client
    op = None
    payload_path = None
    payload = None
    proxy_uri = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:", ["help", "operation=", "payload_path=", "payload=",
                                                               "payload_file=", "proxy-uri-header="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-o", "--operation"):
            op = a
        elif o in ("-p", "--path"):
            payload_path = a
        elif o in ("-P", "--payload"):
            payload = a
        elif o in ("-f", "--payload-file"):
            with open(a, 'r') as f:
                payload = f.read()
        elif o in ("-u", "--proxy-uri-header"):
            proxy_uri = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)

    if op is None:
        print "Operation must be specified"
        usage()
        sys.exit(2)

    if payload_path is None:
        print "Path must be specified"
        usage()
        sys.exit(2)

    if not payload_path.startswith("coap://"):
        print "Path must be conform to coap://host[:port]/path"
        usage()
        sys.exit(2)

    if proxy_uri and not proxy_uri.startswith("http://") and not proxy_uri.startswith("https://"):
        print "Proxy-Uri header must be conform to http[s]://host[:port]/path"
        usage()
        sys.exit(2)

    host, port, payload_path = parse_uri(payload_path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    # Setup client side DTLS socket
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _sock = wrap_client(_sock,
                        cert_reqs=ssl.CERT_REQUIRED,
                        ca_certs=path.join(cert_path, "ca-cert.pem"),
                        ciphers="RSA",
                        do_handshake_on_connect=True)

    client = HelperClient(server=(host, port), sock=_sock,)
    if op == "GET":
        if payload_path is None:
            print "Path cannot be empty for a GET request"
            usage()
            sys.exit(2)
        response = client.get(payload_path)
        print response.pretty_print()
        client.stop()
    elif op == "OBSERVE":
        if payload_path is None:
            print "Path cannot be empty for a GET request"
            usage()
            sys.exit(2)
        client.observe(payload_path, client_callback_observe)

    elif op == "DELETE":
        if path is None:
            print "Path cannot be empty for a DELETE request"
            usage()
            sys.exit(2)
        response = client.delete(payload_path, proxy_uri=proxy_uri)
        print response.pretty_print()
        client.stop()
    elif op == "POST":
        if payload_path is None:
            print "Path cannot be empty for a POST request"
            usage()
            sys.exit(2)
        if payload is None:
            print "Payload cannot be empty for a POST request"
            usage()
            sys.exit(2)
        response = client.post(payload_path, payload, proxy_uri=proxy_uri)
        print response.pretty_print()
        client.stop()
    elif op == "PUT":
        if payload_path is None:
            print "Path cannot be empty for a PUT request"
            usage()
            sys.exit(2)
        if payload is None:
            print "Payload cannot be empty for a PUT request"
            usage()
            sys.exit(2)
        response = client.put(payload_path, payload, proxy_uri=proxy_uri)
        print response.pretty_print()
        client.stop()
    elif op == "DISCOVER":
        response = client.discover()
        print response.pretty_print()
        client.stop()
    else:
        print "Operation not recognized"
        usage()
        sys.exit(2)


if __name__ == '__main__':  # pragma: no cover
    main()
