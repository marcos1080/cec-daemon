import os
import device
import logging

def getDevices(dir, adapterDevices):
	files = os.listdir(dir)
	devices = []

	# Check in the config directory and load each device.	
	for file in files:
		device = __loadFile(dir + "/" + file, adapterDevices)
		if device == None:
			print('There was an error loading device "' + file + '"')
		else:
			devices.append(device)
	
	# Check to see if there are any devices present and loaded.	
	if len(devices) == 0:
		print("No devices found.")
		logging.error("No devices found.")
		return False
	else:
		return devices
		
def __loadFile(device_path, adapterDevices):
	deviceAttr = []
	inputAttr = []

	# Load file into variable lists.
	file = open(device_path, 'r')

	for line in file:
		if line.strip().lower() == '[device]':
			section = "DEVICE"
		elif line.strip().lower() == '[inputs]':
			section = "INPUTS" 
		elif line.strip() != "":	
			if section == "DEVICE":
				result = __addAttribute(line)
				if result != False:
					# Load config name and type
					if result[0] == "name":
						configName = result[1].lower()
					if result[0] == "type":
						configType = result[1].lower()
					
			if section == "INPUTS":
				result = __addAttribute(line)
				if result != False:
					inputAttr.append(result)
	
	file.close()		
	
	# Check that the name and type match the vendor and osd string from cec-client.
	foundName = False
	foundType = False
			
	for dev in adapterDevices:
		for attribute in dev:
			if attribute[0] == "vendor" and attribute[1].lower() == configName:
				deviceName = attribute[1].lower()
				foundName = True
			if attribute[0] == "osd string" and attribute[1].lower() == configType:
				deviceType = attribute[1].lower()
				foundType = True
			if foundName == True and foundType == True:
				break

	# Exit if the name/vendor or type/osd string.
	if foundName == False or foundType == False:
		print('No matching device found for "' + device_path + '"')
		return None
	
	# Get the ID and address attribute.
	for attribute in dev:
		if attribute[0] == "id":
			deviceID = attribute[1].lower().strip()
		if attribute[0] == "address":
			deviceAddress = attribute[1].lower().strip()
	
	return device.Device(deviceID, deviceName, deviceType, deviceAddress, inputAttr)

# Parse config file line.			
def __addAttribute(line):
	attribute = line.split("=")
	if len(attribute) == 2 and attribute[1].strip() != "":
		return (attribute[0].lower().strip(), attribute[1].lower().strip())
	else:
		return False
