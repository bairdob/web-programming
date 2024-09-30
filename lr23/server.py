import sys
from xmlrpc.server import SimpleXMLRPCServer

from calculator import Calculator
from settings import HOST, PORT

with SimpleXMLRPCServer((HOST, PORT)) as server:
    server.register_function(lambda: 'pong', 'ping')
    server.register_instance(Calculator())
    server.register_multicall_functions()
    print(f'Serving XML-RPC on localhost port {PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
