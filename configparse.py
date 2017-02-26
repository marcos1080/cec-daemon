class CreateConfig:

	def __init_(self):
		self.user = None
		self.password = None
		self.port = None
		
def parseConfig(path):
	user = None
	password = None
	port = None
	
	file = open(path, "r")
	
	for line in file:
		option = line.strip().split("=")
		if option[0].lower().strip() == "user" and len(option) == 2:
			if option[1].strip() == "":
				print("No username supplied in the config file.")
			elif len(option[1].strip()) > 20:
				print("Username cannot be more than 20 characters long")
				exit(20)
			else:
				user = option[1].strip()
			
		if option[0].lower().strip() == "password" and len(option) == 2:
			if option[1].strip() == "":
				print("No password supplied in the config file.")
			elif len(option[1].strip()) > 50:
				print("Password cannot be more than 50 characters long")
				exit(20)
			else:
				password = option[1].strip()
		
		if option[0].lower().strip() == "port" and len(option) == 2:
			if option[1].strip() == "":
				print("No port supplied in the config file.")
			else:
				try:
					int(option[1].strip())
					proposed = int(option[1].strip())
					if proposed >= 49152 and proposed <= 65535:
						port = proposed
					else:
						print("Port must be between 49152 and 65535")
				except ValueError:
					print("Port supplied in the config file is not a number.")			
	
	file.close()
	
	if user == None and password == None and port == None:
		print("There are no valid options in the config file or there is an error in the syntax.")

	config = CreateConfig()
	config.user = user
	config.password = password
	config.port = port
		
	return config
