"""
This module contains the code that allows the master to manage 
the slave pins.
"""
# Import configuration
from app import conf as conf

# DAOs
pinDao = __import__(conf["PIN_DAO_NAME"])

# Methods
def getPinData():
    return pinDao.getPinData()

def getPins(host):
    return pinDao.getPins(host)

def getPin(host, pin):
    return pinDao.getPin(host, pin)
    
def addPins(host, pinData):
    pinDao.addPins(host, pinData)

def updatePin(host, pinId, mode, value):
    pinDao.update(host, pinId, mode, value)

def updatePins(host, pinData):
    pinDao.updatePins(host, pinData)

def deletePins(host):
    pinDao.deletePins(host)
