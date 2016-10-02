import SocketServer
import sys
import sqlite3
import parse_expressions
import variables
 

if len(sys.argv) >= 3:
	if not variables.check_admin(sys.argv[2]):
		sys.exit("Enter admin password")
else:
	if not variables.check_admin('admin'):
		sys.exit("Enter admin password")


class EchoRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		while 1:
			self.data = self.request.recv(1024)
			self.request.send(self.data.upper())


statusCodes = []
curUser = ''
def getUserInput():
	message = raw_input()
	while message != "***":
		print "Sending: '%s'" % message
		len_sent = s.send(bytes(message))
		response = s.recv(len_sent)
		print "Received'%s'" % response
		print "type:"
		parse_expressions.parse_expression(message)
		message = raw_input()
	print(userInputs)
	getUserInput()

if __name__ == "__main__":
	import socket
	import threading
	HOST, PORT = "localhost", int(sys.argv[1])
	server = SocketServer.TCPServer((HOST, PORT), EchoRequestHandler)

	t = threading.Thread(target=server.serve_forever)
	t.setDaemon(True)
	t.start()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	getUserInput()
