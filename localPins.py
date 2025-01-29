"""
This module contains the code that allows the slave to manage 
its own pins.
"""

import RPi.GPIO as GPIO
#import GPIO_mock as GPIO
import json, time
import threading

from app import conf as conf

pin_conf_file = open('./pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

localPins = {}
pwmChannels = {}



def loadPinData():
	global localPins
	
	initPins()
	
	f = open("pinData.json", "r")
	fileText = f.read()
	loadedPins = json.loads(fileText)
	f.close()
	
	for pinId in loadedPins:
		updatePin(pinId, loadedPins[pinId]["mode"], loadedPins[pinId]["value"])

def savePinData():
	global localPins
	
	f = open("pinData.json", "w")
	f.write(json.dumps(localPins))
	f.close()

def setPWM(pinId, value):
	global pwmChannels
	
	print("Servo modified")
	if not pinId in pwmChannels.keys():
		pwmChannels[pinId] = GPIO.PWM(int(pinId), conf["PWM_FREQUENCY_HZ"])
		pwmChannels[pinId].start(0.0)
	pwmChannels[pinId].ChangeDutyCycle(value)
	time.sleep(conf["PWM_SECONDS_DELAY"])

def getPins():
	return localPins

def initPins():
	global localPins
	GPIO.setmode(GPIO.BOARD)
	
	for i in range(1, pin_conf['pinNumber'] + 1):
		iStr = str(i).zfill(2)
		if pin_conf[iStr]:
			mode = "Inactive"
		else:
			mode = "Disabled"
		localPins[iStr] = {"mode": mode, "value": ""}

def updatePin(pinId, mode, value):
	global localPins, pwmChannels
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
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = ""
			savePinData()
			return localPins
		#set Input
		elif mode == "Input":
			if pin["mode"] == "PWM":
				pwmChannels.pop(pinId)
			elif pin["mode"] != "Input":
				GPIO.setup(pinNumber, GPIO.IN)
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = GPIO.input(pinNumber)
			savePinData()
			return localPins
		#set Output
		elif mode == "Output":
			if pin["mode"] in ["Inactive", "Input"]:
				GPIO.setup(pinNumber, GPIO.OUT)
			elif pin["mode"] == "PWM":
				pwmChannels.pop(pinId)
			if value == "On":
				GPIO.output(pinNumber, GPIO.HIGH)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
				savePinData()
				return localPins
			else:
				GPIO.output(pinNumber, GPIO.LOW)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = "Off"
				savePinData()
				return localPins
		#set PWM
		elif mode == "PWM":
			if pin["mode"] in ["Inactive", "Input"]:
				GPIO.setup(pinNumber, GPIO.OUT)
			pwmThread = threading.Thread(target=setPWM, args=(pinId, float(value), ), daemon=False)
			pwmThread.start()
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = value
			savePinData()
			return localPins
		
	# Error
	return localPins

def updateInputPins():
	global localPins
	
	for pinId in localPins:
		if localPins[pinId]["mode"] == "Input":
			localPins[pinId]["value"] = GPIO.input(int(pinId))
	
	savePinData()
	return localPins
