devicesList = []

def getDevices():
	return devicesList

def existsDevice(device):
	global devicesList
	return (device in devicesList)
		

def addDevice(device):
	global devicesList
	devicesList.append(device)

def removeDevice(device):
	global devicesList
	devicesList.remove(device)
