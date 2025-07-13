"""
This module contains the code that allows the master to manage 
the slaves and the slave to identify its master.
"""

# Global variables
master = ""
devicesList = []

# Methods
def getDevices():
	return devicesList

def addDevice(device):
	global devicesList
	devicesList.append(device)
	return devicesList

def deleteDevice(device):
	global devicesList
	devicesList.remove(device)
	return devicesList

def getMaster():
	global master
	return master

def addMaster(ipMaster):
	global master
	master = ipMaster

def deleteMaster():
	global master
	master = ""
