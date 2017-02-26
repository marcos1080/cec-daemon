from subprocess import Popen, PIPE
from time import sleep

class Adapter:

	# constructor
	def __init__(self, program):
		self.__adapter = Popen(program, stdin = PIPE, stdout = PIPE, shell = False, universal_newlines = True)
		self.__nbsr = NonBlockingStreamReader(self.__adapter.stdout)
		self.__waitTillReady()
		self.__cecID = self.__getCecID()
		self.__getDevices()
	
	# Getters and setters.
	def getCecID(self):
		return self.__cecID
		
	def getAddress(self):
		return self.__address
		
	def getVendor(self):
		return self.__vendor
		
	def getName(self):
		return self.__name
		
	def getDevices(self):
		return self.__devices
		
	# Operators
	def __waitTillReady(self):
		reply = False
		
		# Wait for the adapter to be ready
		while reply == False:
			lines = self.getOutput().split("\n")
			for line in lines:
				if line!= "":
					print(line)
					if line.strip() == "waiting for input":
						reply = True	
	
	def __getCecID(self):
		reply = False
		self.sendCommand("self")
		while reply == False:
			lines = self.getOutput().split("\n")
			for line in lines:
				print(line)
				if line.find("Addresses controlled by libCEC") != -1:
					result = line.split(":")[1].strip()
					reply = True
					
		return result
	
	def __getDevices(self):
		finished = False
		# Scan command shows all devices connected to the bus.
		self.sendCommand("scan")
		allDevices = []
		device = 0
		
		# Parse devices
		while finished == False:
			lines = self.getOutput().split("\n")
			for line in lines:
				#print(line)
				if line.find("device #") != -1:
					if device != 0:
						allDevices.append(device)
					CecID = line.split("#")[1].split(":")[0].strip()
					device = [("id", CecID)]
				
				if line.find("address:") != -1:
					device.append(("address", line.split(":")[1].strip()))
					
				if line[:14] == ("active source:"):
					device.append(("active", line.split(":")[1].strip()))
					
				if line.find("vendor:") != -1:
					device.append(("vendor", line.split(":")[1].strip()))
					
				if line.find("osd string:") != -1:
					device.append(("osd string", line.split(":")[1].strip()))
				
				if line.find("power status:") != -1:
					device.append(("power status", line.split(":")[1].strip()))
					
				if line.find("currently active source: ") != -1:
					result = line.split(":")[1].strip()
					finished = True
			
		allDevices.append(device)
		devices = []
					
		for device in allDevices:
			if device[0][1] == self.__cecID:
				for attribute in device:
					if attribute[0] == "address":
						self.__address = attribute[1]
					if attribute[0] == "vendor":
						self.__vendor = attribute[1]
					if attribute[0] == "osd string":
						self.__name = attribute[1]
			else:
				devices.append(device)
				
		self.__devices = devices
	
	def sendCommand(self, command):
		self.__adapter.stdin.write(command)
		self.__adapter.stdin.flush()
		return True
		
	def getOutput(self):
		moreLines = True
		output = ""
		
		while moreLines == True:
			line = self.__nbsr.readline(0.1)
			if line == None:
				moreLines = False
			else:
				output += line
		
		return output

# Creates a thread that monitors the stdout stream from the program.
# Call readline on this object to get the lastest output from the stream.	
from queue import Queue, Empty
from threading import Thread
	
class NonBlockingStreamReader:
	
	def __init__(self, stream):
		self.__stream = stream
		self.__queue = Queue()
		
		def __populateQueue(stream, queue):
			while True:
				line = stream.readline()
				if line:
					queue.put(line)
				else:
					print("Unexpected end of stream")
					break
			exit(1)
		
		self.__thread = Thread(target = __populateQueue, args = (self.__stream, self.__queue))
		self.__thread.start()
		
	def readline(self, timeout = None):
		try:
			return self.__queue.get(block = timeout is not None, timeout = timeout)
		except Empty:
			return None
