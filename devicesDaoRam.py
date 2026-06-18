devicesData = {}

def getDevices():
	global devicesData
	return devicesData

def getDevice(deviceIp):
	global devicesData
	return devicesData[deviceIp]

def isAddedDevice(deviceIp):
	global devicesData
	return (deviceIp in devicesData)
	
def addDevice(deviceIp, description, lastUpdate, alive):
	global devicesData
	devicesData[deviceIp] = {"deviceIp": deviceIp, "description": description,
	"lastUpdate": lastUpdate, "alive": alive }

def updateDevice(deviceIp, description, lastUpdate, alive):
	global devicesData
	devicesData[deviceIp] = {"deviceIp": deviceIp, "description": description,
	"lastUpdate": lastUpdate, "alive": alive }

def deleteDevice(deviceIp):
	global devicesData
	devicesData.pop(deviceIp)
