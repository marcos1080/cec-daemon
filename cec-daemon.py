#-----------------------------------------------------------------------------#
#                               Base Directories                              #
#-----------------------------------------------------------------------------#
import os

# Get directory of this script.
base_dir = os.path.dirname(os.path.realpath(__file__))
# Set script file paths.
log_path = base_dir + "/log/cec-daemon.log"
config_path = base_dir + "/config.ini"
device_dir = base_dir + "/devices"

#-----------------------------------------------------------------------------#
#                         Parse Command Line Arguments                        #
#-----------------------------------------------------------------------------#
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default=config_path, help="location of config file")
parser.add_argument("-l", "--log", default=log_path, help="location of log file")
parser.add_argument("-p", "--port", type=int, help="port number to listen on")
args = parser.parse_args()

#-----------------------------------------------------------------------------#
#                                Set up logging                               #
#-----------------------------------------------------------------------------#
import logging

if args.log != None:
	log_dir = os.path.dirname(args.log)
	if os.path.exists(log_dir) == False:
		print('the directory "' + log_dir + '" for the log does not exist.')
		exit(10)
	log_path = args.log
	
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", filename=log_path, level=logging.DEBUG)

#----------------------------------------------------------------------------#
#                              Parse Config File                             #
#----------------------------------------------------------------------------#
import configparse

if args.config != None:
	config_dir = os.path.dirname(args.config)
	if os.path.exists(config_dir) == False:
		print('the directory "' + config_dir + '" for the log does not exist.')  
		exit(11) 
	config_path = args.config
	
config = configparse.parseConfig(config_path)

#----------------------------------------------------------------------------#
#                              Validate Variables                            #
#----------------------------------------------------------------------------#

if config.user == None:
	exit(2)
else:
	user = config.user

if config.password == None:
	exit(2)
else:
	password = config.password

if config.port == None and args.port == None:
	exit(2)
elif args.port != None:
	port = args.port
else:
	port = config.port

#-----------------------------------------------------------------------------#
#                                Set up Adapter                               #
#-----------------------------------------------------------------------------#
import adapter

adapter = adapter.Adapter("/usr/bin/cec-client")

#-----------------------------------------------------------------------------#
#                                Set up Devices                               #
#-----------------------------------------------------------------------------#
import loadDevices

presentDevices = adapter.getDevices()
devices = loadDevices.getDevices(device_dir, presentDevices)
for device in devices:
	device.print()

#-----------------------------------------------------------------------------#
#                                  Main Loop                                  #
# Ctrl^C exits program.                                                       #
#-----------------------------------------------------------------------------#
import connection
from utilityFunctions import verifyClient, processCommand

try:

	conn = connection.Connection(port)
	print("listening on port: " + str(port))
	
	while True:
		client_address = conn.listen()
		loginResult = verifyClient(conn, client_address, user, password)
		if loginResult == True:
			message = conn.receive()
			if message == False:
				conn.send("Error processing data.")
			else:
				result = processCommand(adapter, devices, message)
				conn.send(result)
				print(result)
				adapter.getOutput()
		
	conn.close()	
	
except KeyboardInterrupt:
	print(" signal caught. Exiting...")
	conn.close()
except ValueError or AttributeError:
	conn.close()
