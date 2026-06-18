"""
This module contains the code that allows the slave to manage 
its own pins.
"""
# External modules
import json, utils

# Configuration
conf = utils.getGeneralConfiguration()

# Dinamic modules
localPinsImpl = __import__(conf["LOCAL_PINS_IMPL_NAME"])

# Methods

def loadPins():
	localPinsImpl.loadData()

def getPins():
	return localPinsImpl.getPins()

def updatePin(pinId, description, mode, value):
	return localPinsImpl.updatePin(pinId, description, mode, value)

def updateInputPins():
	return localPinsImpl.updateInputPins()
