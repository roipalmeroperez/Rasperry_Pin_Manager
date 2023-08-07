pinList = {}

def getPins():
	return pinList

def add(pinId, mode, value):
	global pinList
	pinList[pinId] = {
		"mode": mode,
		"value": value
		}
	
def getPin(pinId):
	global pinList
	return pinList[pinId]

def update(pinId, mode, value):
	global pinList
	pinList[pinId] = {
		"mode": mode,
		"value": value
		}


