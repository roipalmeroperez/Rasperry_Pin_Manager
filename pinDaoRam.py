pinList = {}

def getPinData():
	return pinList

def getPins(host):
	return pinList[host]

def addPins(host, pinData):
	global pinList
	pinList[host] = pinData
	
def getPins(host):
	global pinList
	return pinList[host]

def update(host, pinId, mode, value):
	global pinList
	pinList[host][pinId] = {
		"mode": mode,
		"value": value
		}

def updatePins(host, pinData):
	global pinList
	pinList[host] = pinData

def deletePins(host):
	global pinList
	pinList.pop(host)
