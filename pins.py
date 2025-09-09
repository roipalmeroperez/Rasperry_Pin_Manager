"""
This module contains the code that allows the master to manage 
the slave pins.
"""
# Imports
import json

# Configuration
conf_file = open('./config.json')
conf = json.loads(conf_file.read())

# DAOs
pinsDao = __import__(conf["PINS_DAO_NAME"])

# Methods
def getPinData():
    return pinsDao.getPinData()

def getPins(host):
    return pinsDao.getPins(host)

def getPin(host, pin):
    return pinsDao.getPin(host, pin)
    
def addPins(host, pinData):
    pinsDao.addPins(host, pinData)

def updatePin(host, pinId, mode, value):
    pinsDao.update(host, pinId, mode, value)

def updatePins(host, pinData):
    pinsDao.updatePins(host, pinData)

def deletePins(host):
    pinsDao.deletePins(host)
