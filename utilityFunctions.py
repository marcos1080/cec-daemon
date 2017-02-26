import logging
import os
from time import sleep

def verifyClient(connection, address, user, password):
	
	login_credentials = connection.receive()
	
	if login_credentials == False:
			print("There was an error receiving the login data.")
			return False
	
	if login_credentials[0] != "LOGIN":
		print("Data received is not login information.")
		return False
	else:
		login_credentials = login_credentials[1].split(":")
			
	if len(login_credentials) != 2:
		print("wrong number of arguments.")
		return False
	
	# Check if client supplied username is valid.	
	remote_user = login_credentials[0]
	if remote_user == "":
		print("No username supplied.")
		sendLoginFail(connection)
	if len(remote_user) > 20:
		print("Supplied username is greater than 20 characters.")
		sendLoginFail(connection)
	if remote_user[0].isdigit() == True:
		print("Supplied username cannot start with a number.")
		sendLoginFail(connection)
	if remote_user.isalnum == False:
		print("Supplied username must contain letters and numbers only.")
		sendLoginFail(connection)
						
	remote_password = login_credentials[1]
	if remote_password == "":				
		print("no password supplied")
		sendLoginFail(connection)
	if len(remote_password) > 50:
		print("supplied password is greater than 50 characters.")
		sendLoginFail(connection)
		
	if remote_user != user:
		print("Client username does not match.")
		sendLoginFail(connection)
	if remote_password != password:
		print("Client password does not match.")
		sendLoginFail(connection)

	connection.send("LOGGEDON")
	return True

def sendLoginFail(connection):
	connection.send("LOGFAIL")
	return False	

def processCommand(adapter, devices, message):
	
	changeSource = "82"
	broadcast = "f"
	
	request = message[0]
	message = message[1]
	
	if request == "SEND":
		message = message.split(":")
		targetDevice = message[0]
		remoteCommand = message[1]
	
		# Check if device exists in device directory
		for device in devices:
			if device.getDeviceName() == targetDevice:
				break
			else:
				return 'Device "' + targetDevice + '" not found!'
				
		deviceID = str(device.getCecID())
	
		# If command is power then toggle.
		command = "power"
		if remoteCommand.lower() == command:
			# Get TV status
			state = checkDevicePowerStatus(devices, adapter)
			if state == "ON":
				adapter.sendCommand("standby " + deviceID)
			else:
				adapter.sendCommand("on " + deviceID)
			return "Command executed."
		
		command = "input"
		if remoteCommand.lower()[:len(command)] == command:
			inputNumber = remoteCommand.strip()[len(command):]
			inputString = device.getInput(inputNumber)
			if inputString != False:
				adapter.sendCommand("tx " + adapter.getCecID() + broadcast + ":" + changeSource + ":" + inputString)
				device.setCurrentInput(inputNumber)
				sleep(0.2)
				print(adapter.getOutput())
				return "Command executed."
			else:
				return "Input not found!"			
		
		command = "nextinput"
		if remoteCommand.lower() == command:
			currentInput = device.getCurrentInput()
			newInput = str(int(currentInput) + 1)
			inputString = device.getInput(newInput)
			if inputString == False:
				newInput = "1"
				inputString = device.getInput(newInput)
				if inputString == False:
					return "There was an error, input cannot be changed!"
			adapter.sendCommand("tx " + adapter.getCecID() + broadcast + ":" + changeSource + ":" + inputString)
			device.setCurrentInput(newInput)
			sleep(0.2)
			print(adapter.getOutput())
			return "Command executed."				
		
	if request == "GET":
	
		if message == "LIST":
			device_list = ""
			for device in devices:
				device_list += device.getDetails()
				
			return device_list
			
	return "Command not valid!"
			
def checkDevicePowerStatus(devices, adapter):
	
	adapter.getOutput()
	for device in devices:
		adapter.sendCommand("tx " + adapter.getCecID() + device.getCecID() + ":8f")
		reply = False
		
		while reply == False:
			lines = adapter.getOutput().split("\n")
			for line in lines:
				if line[:9] == "TRAFFIC: ":
					print(line)
					line = line.split(">>")
					if len(line) == 2:
						reply = True
						break

							
		return_code = line[1].strip()
		if return_code == device.getCecID() + adapter.getCecID() + ":90:00":
			return "ON"
		else:
			return "OFF"
		
				
