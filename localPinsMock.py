import json, time, random

from app import conf as conf

pin_conf_file = open('./pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

localPins = {}

def getPins():
	return localPins

def loadPinData():
	initPins()

def initPins():
	global localPins
	
	for i in range(1, pin_conf['pinNumber'] + 1):
		iStr = str(i).zfill(2)
		if pin_conf[iStr]:
			mode = "Inactive"
		else:
			mode = "Disabled"
		localPins[iStr] = {"mode": mode, "value": ""}

def updatePin(pinId, mode, value):
	"""global localPins
	
	localPins[pinId]["mode"] = mode
	localPins[pinId]["value"] = value
	
	return localPins"""
	global localPins, pwmChannels
	pin = localPins[pinId]
	pinNumber = int(pinId)
	
	if pin["mode"] == "Disabled":
		return localPins
	elif mode in ["Disabled", "Inactive", "Input", "Output", "PWM"]:
		# set Disabled, Inactive or PWM
		if mode in ["Disabled", "Inactive", "PWM"]:
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = ""
		#set Input
		elif mode == "Input":
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = random.randint(0, 9)
		#set Output
		elif mode == "Output":
			if value in ["On", "Off"]:
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
		
		return localPins

def updateInputPins():
	global localPins
	
	for pinId in localPins:
		if localPins[pinId]["mode"] == "Input":
			localPins[pinId]["value"] = random.randint(0, 9)
	
	return localPins

