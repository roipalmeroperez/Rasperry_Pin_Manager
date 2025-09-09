"""
This module contains the code that allows the master to manage 
the slaves and the slave to identify its master.
"""

# Imports
import json, datetime, requests, socket
import utils, pins

# Configuration
conf_file = open('./config.json')
conf = json.loads(conf_file.read())

# DAOs
devicesDao = __import__(conf["DEVICES_DAO_NAME"])

# Methods

# Global variables
devicesList = []

# Methods
def getDevices():
	return devicesDao.getDevices()

def addDevice(deviceIp, description):
	if devicesDao.isAddedDevice(deviceIp):
		return 200
	
	else:
		#try:
			url = "http://" + deviceIp + ":" + str(conf["SLAVE_PORT"]) + "/master"
			response = requests.post(url)
			deviceIp = json.loads(response.text)["ip"]
			url = "http://" + deviceIp + ":" + str(conf["SLAVE_PORT"]) + "/pins"
			response = requests.get(url)
			data = json.loads(response.text)
			lastUpdate = datetime.datetime.now()
			alive = True
			devicesDao.addDevice(deviceIp, description, lastUpdate, alive)
			pins.addPins(deviceIp, data)
			return 201
		#except:
			#return 404

def deleteDevice(deviceIp):
	if not devicesDao.isAddedDevice(deviceIp):
		return 404
	
	else:
		pins.deletePins(deviceIp)
		devicesDao.deleteDevice(deviceIp)
		try:
			url = "http://" + deviceIp + ":" + str(conf["SLAVE_PORT"]) + "/master"
			response = requests.delete(url)
			return 200
		except:
			return 404

def updateDevice(deviceIp, description, lastUpdate, alive):
	pass
