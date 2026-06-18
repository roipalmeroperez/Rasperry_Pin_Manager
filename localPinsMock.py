# Imports
import json, random
import utils

# Import configuration
pin_conf = utils.getPinConfiguration()

# Global variables
localPinsData = {}

# Methods
def initData():
	data = {}
	
	for i in range(1, pin_conf['pinNumber'] + 1):
		iStr = str(i).zfill(2)
		if pin_conf[iStr]:
			mode = "Inactive"
		else:
			mode = "Disabled"
		data[iStr] = {"mode": mode, "value": ""}
	return data

def loadData():
	savePinData(initData())

def savePinData(data):
	global localPinsData
	localPinsData = data

def getPins():
	global localPinsData
	return localPinsData

def updatePin(pinId, description, mode, value):
	"""localPins = getPins()
	pin = localPins[pinId]
	pinNumber = int(pinId)
	
	if pin["mode"] == "Disabled":
		return localPins
	elif mode in ["Disabled", "Inactive", "Input", "Output", "PWM"]:
		# set Disabled or Inactive
		if mode in ["Disabled", "Inactive"]:
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = ""
			savePinData(localPins)
			return localPins
		#set Input
		elif mode == "Input":
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = str(random.randint(0, 1))
			savePinData(localPins)
			return localPins
		#set Output
		elif mode == "Output":
			if value in ["On", "Off"]:
				localPins[pinId]["description"] = description
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
				savePinData(localPins)
				return localPins
		#set PWM
		elif mode == "PWM":
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = value
			savePinData(localPins)
			return localPins
		
	# Error
	return localPins"""
	
	localPins = getPins()
	pin = localPins[pinId]
	pinNumber = int(pinId)
	
	if (pin["mode"] == "Disabled") and (mode == "Disabled"):
		localPins[pinId]["description"] = description
		savePinData(localPins)
		return localPins
	elif pin["mode"] == "Disabled":
		return localPins
	elif pin["mode"] == "Inactive":
		if mode in ["Disabled", "Inactive"]:
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			savePinData(localPins)
			return localPins
		elif mode == "Input":
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = str(random.randint(0, 1))
			savePinData(localPins)
			return localPins
		elif mode == "Output":
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			if value == "1":
				localPins[pinId]["value"] = "1"
			else:
				localPins[pinId]["value"] = "0"
			savePinData(localPins)
			return localPins
		elif mode == "PWM":
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = value
			savePinData(localPins)
			return localPins
	elif mode in ["Disabled", "Inactive"]:
		localPins[pinId]["description"] = description
		localPins[pinId]["mode"] = mode
		localPins[pinId]["value"] = ""
		savePinData(localPins)
		return localPins
	elif (pin["mode"] == "Input") and (mode == "Input"):
		localPins[pinId]["description"] = description
		localPins[pinId]["value"] = str(random.randint(0, 1))
		savePinData(localPins)
		return localPins
	elif (pin["mode"] == "Output") and (mode == "Output"):
		localPins[pinId]["description"] = description
		if value == "1":
			localPins[pinId]["value"] = "1"
		else:
			localPins[pinId]["value"] = "0"
		savePinData(localPins)
		return localPins
	elif (pin["mode"] == "PWM") and (mode == "PWM"):
		localPins[pinId]["description"] = description
		localPins[pinId]["value"] = value
		savePinData(localPins)
		return localPins
	# Error
	return localPins

def updateInputPins():
	localPins = getPins()
	
	for pinId in localPins:
		if localPins[pinId]["mode"] == "Input":
			localPins[pinId]["value"] = str(random.randint(0, 1))
	
	savePinData(localPins)
	return localPins
