#from app import conf as conf
import requests


master = ""

devicesList = []

def getDevices():
	return devicesList

def addDevice(device):
	global devicesList
	
	if device in devicesList:
		return 200
	try:
		url = "http://" + device + "/servers"
		response = requests.post(url)
	except:
		return 404
	
	devicesList.append(device)
	
	return 201

def deleteDevice(device):
	global devicesList
	
	if not(device in devicesList):
		return 404
	else:
		devicesList.remove(device)
		try:
			url = "http://" + device + "/servers"
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

def deleteMaster(ipMaster):
	global master
	if master == ipMaster:
		master = ""
