import socket
import sys
import create2api

class RequestError(Exception):
    def __init__(self, message, *errors):

        # Call the base class constructor with the parameters it needs
        super(RequestError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors

class Client(object):
	"""While this is just a simple wrapper around the socket interface
		it is meant to be easy to use and also act as an example on how to
		write or extend the client interface
	"""
	
	def __init__(self, host = '127.0.0.1', port = 8888):
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print('Socket created')

		#connect socket to host on port
		try:
			self.sock.connect((host, port))
		except socket.error as msg:
			print('connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

		print('Sucessfully Connected')
		self.readFile = self.sock.makefile("r")
		if self.windows:
			atexit.register(self.close)

	def __del__(self):
		if self.windows:
			self.close()
			try:
				atexit.unregister(self.close)
			except:
				pass   

	def close(self):
		"""Closes up serial ports and terminates connection to the Create2Server
		"""
		try:
			self.socket.close()
		except:
			pass

	def send(self, *args):
			self.conn.send(create2api.make_command_string(args).encode('utf-8'))

	def receive(self):
		"""Receives data. Note that the trailing newline '\n' is trimmed"""
		val = self.readFile.readline().rstrip("\n")
		return val

	def sendReceive(self, *data):
		"""Sends and receive data"""
		self.send(*data)
		return self.receive()