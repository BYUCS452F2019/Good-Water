import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


    #This class is responsible for making API endpoints that
    # will receive JSON objects and then call DAO methods such as "addUser"
    # "addBuildling" etc.
