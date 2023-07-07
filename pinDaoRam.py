import json

pin_conf_file = open('./pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

pinList = {}

def getPins():
	return pinList

def add(pinId, name, enabled, mode, value):
	global pinList
	pinList[pinId] = {
		"name": name,
		"mode": mode,
		"value": value
		}
	
def getPin(pinId):
	global pinList
	return pinList[pinId]

def update(pinId, name, mode, value):
	global pinList
	pinList[pinId] = {
		"name": name,
		"mode": mode,
		"value": value
		}


