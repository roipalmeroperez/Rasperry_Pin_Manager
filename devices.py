"""
This module contains the code that allows the master to manage 
the slaves and the slave to identify its master.
"""

#from app import conf as conf
import requests, pins


master = ""

devicesList = []

def getDevices():
	return devicesList

def addDevice(device):
	global devicesList
	
	if device in devicesList:
		return 200
	try:
		url = "http://" + device + "/master"
		response = requests.post(url)
	except:
		return 404
	
	url = "http://" + device + "/pins"
	response = requests.get(url)
	pins.addPins(device, response.text)
	
	devicesList.append(device)
	
	
	return 201

def deleteDevice(device):
	global devicesList
	
	if not(device in devicesList):
		return 404
	else:
		devicesList.remove(device)
		try:
			url = "http://" + device + "/master"
			response = requests.delete(url)
		except:
			return 404
	
	return 200

def getMaster():
	global master
	return master

def addMaster(ipMaster):
	global master
	master = ipMaster

def deleteMaster():
	global master
	master = ""
