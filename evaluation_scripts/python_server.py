#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)
        cwd = os.getcwd()
        print(cwd)
        f = open(cwd + "/evaluation_scripts/text.txt", 'rb')
        self.send_header('Content-type',    'text/html')
        print("Sending")
        # self.send_header('Content-type',    'text/html')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return
 
def run():
    print('starting server...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8020)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()
    
 
run()