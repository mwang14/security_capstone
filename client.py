import socket
import sys

HOST, PORT = "localhost", int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))
data = raw_input()
while True:
	sock.sendall(data)
	data = raw_input()
	received = sock.recv(1024)
	print received
