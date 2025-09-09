"""
This module contains the code that allows the slave to manage 
its own pins.
"""
# External modules
import json

# Configuration
conf_file = open('./config.json')
conf = json.loads(conf_file.read())

# Dinamic modules
localPinsImpl = __import__(conf["LOCAL_PINS_IMPL_NAME"])

# Methods

def loadData():
	localPinsImpl.loadData()

def getPins():
	return localPinsImpl.getPins()

def updatePin(pinId, mode, value):
	return localPinsImpl.updatePin(pinId, mode, value)

def updateInputPins():
	return localPinsImpl.updateInputPins()
