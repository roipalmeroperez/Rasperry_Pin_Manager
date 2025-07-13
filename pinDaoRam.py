"""
This module contains the DAO code that allows the system pin 
information to be stored in RAM memory.
"""

# Global variables
pinList = {}

# Methods
def getPinData():
	global pinList
	return pinList

def getPins(host):
	global pinList
	return pinList[host]

def getPin(host, pin):
	global pinList
	return pinList[host][pin]

def addPins(host, pinData):
	global pinList
	pinList[host] = pinData

def deletePins(host):
	global pinList
	pinList.pop(host)

def update(host, pinId, mode, value):
	global pinList
	pinList[host][pinId] = {
		"mode": mode,
		"value": value
		}

def updatePins(host, pinData):
	global pinList
	pinList[host] = pinData
