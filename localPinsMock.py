import json, time

from app import conf as conf

pin_conf_file = open('./pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

localPins = {}

def getPins():
	return localPins

def initPins():
	global localPins
	
	for i in range(1, pin_conf['pinNumber'] + 1):
		iStr = str(i).zfill(2)
		if pin_conf[iStr]:
			mode = "Inactive"
		else:
			mode = "Disabled"
		localPins[iStr] = {"mode": mode, "value": "-"}

def updatePin(pinId, mode, value):
	global localPins
	
	localPins[pinId]["mode"] = mode
	localPins[pinId]["value"] = value
	
	return localPins

def updateInputPins():
	global localPins
	
	for pinId in localPins:
		if localPins[pinId]["mode"] == "Input":
			localPins[pinId]["value"] = "-"
	
	return localPins
	
if __name__ == '__main__':
	initPins()
	print(getPins())
	#localPins["10"]["mode"] = "Input"
	#localPins["12"]["mode"] = "Input"
	updateInputPins()
	print(getPins())
	
	
