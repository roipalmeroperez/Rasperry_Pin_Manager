import RPi.GPIO as GPIO
import json
from app import conf as conf

pinList = {}
pin_conf_file = open('./pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

pinDao = __import__(conf["PIN_DAO_NAME"])


class Pin:
    def __init__(self, pinId, pinType, mode):
        self.pinId = pinId
        self.mode = mode

class NotAllowedPinException(Exception):
    "Exception raised for illegal pin assignment"
    
    def __init__(self):
        self.message = "Illegal pin assignment"
        super().__init__(self.message)

def init():
    GPIO.setmode(GPIO.BOARD)
    initPinData()

def isValid(pin):
    if pin < 1 or pin > pin_conf['pinNumber']:
        return False
    return True

def initPinData():
    for i in range(1, pin_conf['pinNumber'] + 1):
        iStr = str(i)
        if pin_conf[iStr]:
            mode = "Inactive"
        else:
            mode = "Disabled"
        pinDao.add("pin" + iStr, iStr, pin_conf[iStr], mode, "-")

def getPins():
    return pinDao.getPins()

def updatePin(pinId, name, mode, value):
    if isValid(int(name)):
        pin = pinDao.getPin(pinId)
        if pin["mode"] != "Disabled":
            pinDao.update(pinId, name, mode, value)

def updateInputPins():
    pinData = getPins()
    for pinId in pinData:
        pin = pinData[pinId]
        if pin["mode"] == "Input":
            #pin["value"] = GPIO.input(pin["name"])
            pin["value"] = "Input"
            pinDao.update("pin" + pin["name"], pin["name"], pin["mode"], pin["value"])
            

"""
def setOut(pinStr):
    pin = int(pinStr)
    if isValid(pin):
        GPIO.setup(pin, GPIO.OUT)
        pinList['pin' + pinStr]['mode']= "Output"
        pinList['pin' + pinStr]['value']= "Off"

def setIn(pinStr):
    pin = int(pinStr)
    if isValid(pin):
        GPIO.setup(pin, GPIO.IN)
        pinList['pin' + pinStr]['mode']= "Input"
        pinList['pin' + pinStr]['value']= "-"

def on(pinStr):
    GPIO.output(int(pinStr), GPIO.HIGH)
    pinList['pin' + pinStr]['value']= "On"
    
def off(pinStr):
    GPIO.output(int(pinStr), GPIO.LOW)
    pinList['pin' + pinStr]['value']= "Off"
    
def clear(pinStr):
    pin = int(pinStr)
    GPIO.cleanup(pin)
    pinList['pin' + pinStr]['mode']= "-"
    pinList['pin' + pinStr]['value']= "-"

"""

if __name__ == '__main__':
    # Tests
    print("Number of pins: " + str(pin_conf['pinNumber']))
    init()
    #raise NotAllowedPinException
    #setOut('25')
    print("Pin 13 enable: " + str(isValid('13')))
    print("Pin 13 enable: " + str(pin_conf['13']))
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    print("Pin 13 on")
    GPIO.output(13, GPIO.HIGH)
    print("Pin 13 off")
    GPIO.output(13, GPIO.LOW)
    print("Clear pin 13")
    clear("13")
    print("Clear pin 13")
    clear("13")
    print("Pin 25 enable: " + str(pin_conf['25']))
    print(pinList)
    #on(16)
    #GPIO.setup(5, GPIO.OUT)
