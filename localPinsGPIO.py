"""
This module contains the code that allows the slave to manage 
its own pins.
"""
# Imports
import RPi.GPIO as GPIO
import json, time, threading
import utils

# Import configuration
pin_conf = utils.getPinConfiguration()

# Global variables
pwmChannels = {}


# Methods
def initData():
	data = {}
	
	for i in range(1, pin_conf['pinNumber'] + 1):
		iStr = str(i).zfill(2)
		if pin_conf[iStr]:
			mode = "Inactive"
		else:
			mode = "Disabled"
		data[iStr] = {"description": "", "mode": mode, "value": ""}
	return data

def loadData():
	loadedPins = getPins()
	savePinData(initData())
	GPIO.setmode(GPIO.BOARD)
	if loadedPins != {}:
		for pinId in loadedPins:
			updatePin(pinId, loadedPins[pinId]["description"], loadedPins[pinId]["mode"], loadedPins[pinId]["value"])

def savePinData(data):
	f = open("localPinsData.json", "w")
	f.write(json.dumps(data))
	f.close()

def setPWM(pinId, value):
	global pwmChannels
	
	if not pinId in pwmChannels.keys():
		pwmChannels[pinId] = GPIO.PWM(int(pinId), pin_conf["PWM_FREQUENCY_HZ"])
		pwmChannels[pinId].start(0.0)
	pwmChannels[pinId].ChangeDutyCycle(value)
	time.sleep(pin_conf["PWM_SECONDS_DELAY"])

def getPins():
	f = open("localPinsData.json", "r")
	fileText = f.read()
	f.close()
	
	return json.loads(fileText)
"""
def updatePin(pinId, description, mode, value):
	global pwmChannels
	localPins = getPins()
	pin = localPins[pinId]
	pinNumber = int(pinId)
	
	if pin["mode"] == "Disabled":
		return localPins
	elif mode in ["Disabled", "Inactive", "Input", "Output", "PWM"]:
		# set Disabled or Inactive
		if mode in ["Disabled", "Inactive"]:
			if pin["mode"] in ["Input", "Output"]:
				GPIO.cleanup(pinNumber)
			elif pin["mode"] == "PWM":
				GPIO.cleanup(pinNumber)
				pwmChannels.pop(pinId)
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = ""
			savePinData(localPins)
			return localPins
		#set Input
		elif mode == "Input":
			if pin["mode"] == "PWM":
				pwmChannels.pop(pinId)
			elif pin["mode"] != "Input":
				GPIO.setup(pinNumber, GPIO.IN)
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = str(GPIO.input(pinNumber))
			savePinData(localPins)
			return localPins
		#set Output
		elif mode == "Output":
			if pin["mode"] in ["Inactive", "Input"]:
				GPIO.setup(pinNumber, GPIO.OUT)
			elif pin["mode"] == "PWM":
				pwmChannels.pop(pinId)
			if value == "On":
				GPIO.output(pinNumber, GPIO.HIGH)
				localPins[pinId]["description"] = description
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
				savePinData(localPins)
				return localPins
			else:
				GPIO.output(pinNumber, GPIO.LOW)
				localPins[pinId]["description"] = description
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = "Off"
				savePinData(localPins)
				return localPins
		#set PWM
		elif mode == "PWM":
			if pin["mode"] in ["Inactive", "Input"]:
				GPIO.setup(pinNumber, GPIO.OUT)
			pwmThread = threading.Thread(target=setPWM, args=(pinId, float(value), ), daemon=False)
			pwmThread.start()
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = value
			savePinData(localPins)
			return localPins
		
	# Error
	return localPins"""

def updatePin(pinId, description, mode, value):
	global pwmChannels
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
			GPIO.setup(pinNumber, GPIO.IN)
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = str(GPIO.input(pinNumber))
			savePinData(localPins)
			return localPins
		elif mode == "Output":
			GPIO.setup(pinNumber, GPIO.OUT)
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			if value == "1":
				localPins[pinId]["value"] = "1"
				GPIO.output(pinNumber, GPIO.HIGH)
			else:
				localPins[pinId]["value"] = "0"
				GPIO.output(pinNumber, GPIO.LOW)
			savePinData(localPins)
			return localPins
		elif mode == "PWM":
			GPIO.setup(pinNumber, GPIO.OUT)
			pwmThread = threading.Thread(target=setPWM, args=(pinId, float(value), ), daemon=False)
			pwmThread.start()
			localPins[pinId]["description"] = description
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = value
			savePinData(localPins)
			return localPins
	elif mode in ["Disabled", "Inactive"]:
		if pin["mode"] in ["Input", "Output"]:
			GPIO.cleanup(pinNumber)
		elif pin["mode"] == "PWM":
			GPIO.cleanup(pinNumber)
			pwmChannels.pop(pinId)
		localPins[pinId]["description"] = description
		localPins[pinId]["mode"] = mode
		localPins[pinId]["value"] = ""
		savePinData(localPins)
		return localPins
	elif (pin["mode"] == "Input") and (mode == "Input"):
		localPins[pinId]["description"] = description
		localPins[pinId]["value"] = str(GPIO.input(pinNumber))
		savePinData(localPins)
		return localPins
	elif (pin["mode"] == "Output") and (mode == "Output"):
		localPins[pinId]["description"] = description
		if value == "1":
			localPins[pinId]["value"] = "1"
			GPIO.output(pinNumber, GPIO.HIGH)
		else:
			localPins[pinId]["value"] = "0"
			GPIO.output(pinNumber, GPIO.LOW)
		savePinData(localPins)
		return localPins
	elif (pin["mode"] == "PWM") and (mode == "PWM"):
		pwmThread = threading.Thread(target=setPWM, args=(pinId, float(value), ), daemon=False)
		pwmThread.start()
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
			localPins[pinId]["value"] = str(GPIO.input(int(pinId)))
	
	savePinData(localPins)
	return localPins
