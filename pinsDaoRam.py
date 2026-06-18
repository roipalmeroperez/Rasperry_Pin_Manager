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

def isPin(host, number):
	global pinList
	if host in pinList:
		return number in pinList[host]
	else:
		return False

def addPins(host, pinData):
	global pinList
	pinList[host] = pinData

def deletePins(host):
	global pinList
	pinList.pop(host)

def updatePins(host, pinData):
	global pinList
	pinList[host] = pinData
