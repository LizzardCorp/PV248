import http.client
from sys import argv
import json

def create_connection(port=8080, host=''):
    conn = http.client.HTTPConnection(host, port)
    conn.request("GET", "/list")
    response = conn.getresponse()
    string = response.read().decode('utf-8')
    print(string)
    conn.close()

if __name__ == '__main__':
    try:
        port = int(argv[2])
        host = argv[1]
        if port < 1:
            print("Third parameter has to be larger than zero")
        elif port > 65535:
            print("Third parameter has to be less than 65536")
        else:
            create_connection(port=port, host=host)
    except ValueError:
        print("Third parameter has to be integer")
