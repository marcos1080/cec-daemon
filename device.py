class Device:
	
	# Constructor
	def __init__(self, ID, name, devType, address, inputAttr):
		self.__ID = ID
		self.__name = name
		self.__devType = devType
		self.__address = address
		self.__inputAttr = inputAttr
		self.__currentInput = "1"
	
	# Getters and Setters	
	def getCecID(self):
		return self.__ID	
		
	def getDeviceName(self):
		return self.__name
				
	def getDeviceType(self):
		return self.__devType
		
	def getAddress(self):
		return self.__address

	def getInput(self, input_number):
		for attribute in self.__inputAttr:
			if attribute[0] == input_number:
				return attribute[1]
		return False
	
	def setCurrentInput(self, inputNumber):
		self.__currentInput = inputNumber
		
	def getCurrentInput(self):
		return self.__currentInput
	
	# Operators	
	def print(self):
		print("Device info:")
		print("ID         :" + self.__ID)
		print("Name       :" + self.__name)
		print("Type       :" + self.__devType)
		print("address	   :" + self.__address)
		print("")
		print("Inputs:")
		for attribute in self.__inputAttr:
			print(attribute[0] + "      :" + attribute[1])
		print("")
			
	def getDetails(self):
		details = "Device info:\n"
		details += "ID         :" + self.__ID + "\n"
		details += "Name       :" + self.__name + "\n"
		details += "Type       :" + self.__devType + "\n"
		details += "address	   :" + self.__address + "\n"
		details += "\n"
		details += "Inputs:\n"
		for attribute in self.__inputAttr:
			details += attribute[0] + "      :" + attribute[1] + "\n"
		details += "\n"
		details += "Current input = " + self.__currentInput
			
		return details
