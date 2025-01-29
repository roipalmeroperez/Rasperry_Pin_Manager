"""
This module contains the code that allows the master to manage 
the slave pins.
"""

import json, requests
from app import conf as conf

pinDao = __import__(conf["PIN_DAO_NAME"])


def getPinData():
    return pinDao.getPinData()

def getPins(host):
    return pinDao.getPins(host)
    
def addPins(host, pinData):
    pinDao.addPins(host, pinData)

def updatePin(host, pinId, mode, value):
    pinDao.update(host, pinId, mode, value)

def updatePins(host, pinData):
    pinDao.updatePins(host, pinData)

def deletePins(host):
    pinDao.deletePins(host)
