import socket
import logging
import hashlib

class Connection:

	# Constructors
	def __init__(self, PORT):
		self.__HOST = socket.gethostname()
		self.__PORT = PORT
		self.__setSocket()
		self.__BUFSIZE = 4096
		self.__STATE = "DOWN"
		self.__client_address = None
		self.__HASHSEP = "<<:#:>>"
		self.__TYPESEP = "<<:>:>>"
		
		print("Socket created using port: " + str(self.__PORT))

	# Setters and Getters
	def getPort(self):
		return self.__PORT

	def setPort(self, PORT):
		if self.__STATE == "UP":
			print("Socket is being used, close the socket to change port.")
			logging.warning("Attempt to change the port of currently active socket!")
			return False
			
		self.__PORT = PORT
		print("Socket reset using: " + str(self.__HOST) + ":" + str(self.__PORT))
		logging.info("Socket values changed from %s:%s to %s:%s", HOST, PORT, self.__HOST, self.__PORT)
		return True

	def getBufferSize(self):
		return self.__BUFSIZE

	def setBufferSize(self, BUFSIZE):
		self.__BUFSIZE = BUFSIZE
	
	def getClientAddress(self):
		return self.__client_address
	
	# Set the socket up, used by the constructor and setPort()
	def __setSocket(self):
		self.__ADDR = (self.__HOST, self.__PORT)
		self.__server_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
		self.__server_socket.bind((self.__ADDR))
		self.__server_socket.listen(5)
		
	##### Operations

	# Close the socket connection, deletes socket variable and sets status to "DOWN"
	def close(self):
		if self.__STATE == "DOWN":
			print("Socket is already down.")
			return False
			
		self.__server_socket.close()
		self.__client_address = None
		print("Socket using port: " + str(self.__PORT) + " deleted")
		self.__STATE = "DOWN"
		return True

	# Wait for a client connection. As soon as one is made the STATUS is set to "UP".
	# Returns the clients address on success and False if there is already a connection.
	def listen(self):
		print("Waiting for connection...")
		self.__connection, self.__client_address = self.__server_socket.accept()
		print("... connection from " + str(self.__client_address))
		# Let the client this connection is ready to receive data.
		self.__connection.send("READY".encode())				
		self.__STATE = "UP"			
		return self.__client_address

	# Send a message.
	# Function first sends the size of the data, then the md5 hash of the data and finally
	# the data itself.
	# Returns True if the client indicates it successfully received the data and False in 
	# any other circumstance.
	def send(self, message):
		if self.__STATE == "DOWN":
			print("Server is down")
			return False
			
		md5sum = hashlib.md5()
		md5sum.update(message.encode())
		message = message + self.__HASHSEP + md5sum.hexdigest()
		message = message.encode()
		
		bytes_sent = 0
		message_size = len(message)
		self.__connection.send(str(message_size).encode())
		
		server_state = self.__connection.recv(self.__BUFSIZE).decode()
		if server_state != "READY":
			print("Server not ready")
			return False
			
		while bytes_sent < message_size:
			sent = self.__connection.send(message[bytes_sent:])
			if sent == 0:
				print("Socket connection broken, file not sent.")
				logging.error("Socket broken, file not sent!")
				self.close()
				return False
			bytes_sent += sent
				
		server_state = self.__connection.recv(self.__BUFSIZE)
		if server_state.decode() == "RECEIVED":
			return True
		else:
			return False
			
	# If a connection is "UP" then wait for data to be sent.
	# Returns the data sent on success and False on any error.
	def receive(self):
		if self.__STATE == "DOWN":
			print("Socket is down, cannot receive files.")
			return False
		
		# If there is a ValueError exception thrown it means the client has shutdown the connection.
		try:
			# The client will send the size of the message to be sent.
			message_size = int(self.__connection.recv(self.__BUFSIZE).decode())
		except ValueError:
			print("Socket connection broken, cannot receive.")
			logging.error("Socket broken, cannot receive!")
			self.__STATE = "DOWN"
			return False	
			
		# Initialise message recepticle and how much data has been received.			
		chunks = []
		bytes_received = 0
		
		# As soon as this is sent the client will start transmitting data.
		self.__connection.send("READY".encode())
		
		# Receive the data. If the data is larger than the buffer size this loop will keep
		# reading the buffer until the whole message is received.
		while bytes_received < message_size:
			chunk = self.__connection.recv(min(message_size - bytes_received, self.__BUFSIZE))
			# If a chunk is empty it means the connection has been broken.
			if chunk == b'':
				print("Socket connection broken, file not received.")
				logging.error("Socket broken, file not received!")
				return False
			chunks.append(chunk)
			bytes_received += len(chunk)
		
		# As soon as the whole message has been received a confirmation is sent to the client.
		message = b''.join(chunks).decode().split(self.__HASHSEP)
		
		md5sum = hashlib.md5()
		md5sum.update(message[0].encode())
		
		if md5sum.hexdigest() == message[1]:
			self.__connection.send("RECEIVED".encode())	
			return message[0].split(self.__TYPESEP)
		else:
			print("md5 sums dont match!")
			return False
	
	# Simply prints the current state.	
	def getStatus(self):
		
		# Print details	
		print("Socket is " + self.__STATE)
		print("Target host address: " + str(self.__HOST))
		print("Target host port:    " + str(self.getPort()))
		
