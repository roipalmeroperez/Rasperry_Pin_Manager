"""
This module contains the code that allows the master to manage 
the slave pins.
"""
# Imports
import utils

# Configuration
conf = utils.getGeneralConfiguration()

# DAOs
pinsDao = __import__(conf["PINS_DAO_NAME"])

# Methods
def getPinData():
    return pinsDao.getPinData()

def getPins(host):
    return pinsDao.getPins(host)

def isPin(host, number):
    return pinsDao.isPin(host, number)
    
def addPins(host, pinData):
    pinsDao.addPins(host, pinData)

def updatePins(host, pinData):
    pinsDao.updatePins(host, pinData)

def deletePins(host):
    pinsDao.deletePins(host)
