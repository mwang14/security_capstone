#/usr/bin/python
import SocketServer
import sys
import sqlite3
import parse_expressions
import variables

statusCodes = []
curUser = ''
 

if len(sys.argv) >= 3:
	if not variables.check_admin(sys.argv[2]):
		sys.exit("Enter admin password")
else:
	if not variables.check_admin('admin'):
		sys.exit("Enter admin password")


class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		while 1:
			self.data = self.request.recv(1024)
			if not self.data:
				break
			parse_expressions.parse_expression(self.data)
			self.request.sendall(str(statusCodes))
if __name__ == "__main__":
	HOST, PORT = "localhost", int(sys.argv[1])
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
