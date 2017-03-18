class Config:

	def __init__(self):
		# Client/Daemon settings.
		self.user = None
		self.password = None
		self.port = None
		
		# cec-client loaction.
		self.program = None
		
		# file locations.
		self.log = None
		
class Argument:

	def __init__(self, key, value):
		self.key = key
		self.value = value
	
		
def parseConfig(path):
	
	def parseLine(line, lineNumber):
		"""
			Parse a line in the config file to see if it contains a valid argument.
		"""
		# Remove anything that is a comment.
		line = line.strip().split("#")[0]
		
		# Separate key from value.
		options = line.strip().split("=")
		
		# Returning none if there not elements.
		if len(options) != 2:
			return None
			
		key = options[0].strip()
		value = options[1].strip()
		
		# Cannot have empty key.
		if key == "":
			print("Empty value found on line " + lineNumber + " in config file.")
			return None
			
		# Key can only have the chars a-z.
		if not key.isalpha():
			print("Key contains invalid character on line " + lineNumber + " in config file.")
			return None
		
		# Otherwise return an argument object.
		argument = Argument(key, value)
		
		return argument
		
	def checkArgument(argument, config):
		value = argument.value
	
		if argument.key == "User":
			if value == "":
				print("No username supplied in the config file.")
			elif len(value) > 20:
				print("Username cannot be more than 20 characters long")
			else:
				config.user = argument.value
			
		elif argument.key == "Password":
			if value == "":
				print("No password supplied in the config file.")
			elif len(value) > 50:
				print("Password cannot be more than 50 characters long")
			else:
				config.password = value
		
		elif argument.key == "Port":
			if value == "":
				print("No port supplied in the config file.")
			else:
				try:
					proposed = int(value)
					if proposed >= 49152 and proposed <= 65535:
						config.port = proposed
					else:
						print("Port must be between 49152 and 65535")
				except ValueError:
					print("Port supplied in the config file is not a number.")	
					
	"""
		Function logic.
	"""	
	# Config to store key/value pairs.
	config = Config()
	
	lineNumber = 0
	file = open(path, "r")
	
	for line in file:
		# If line contains a tuple then check if the values are valid.
		line = parseLine(line, str(lineNumber))
		if line != None:
			checkArgument(line, config)
			
		lineNumber += 1
	
	file.close()
	
	if config.user == None and config.password == None and config.port == None:
		print("There are no valid options in the config file or there is an error in the syntax.")
		
	return config
