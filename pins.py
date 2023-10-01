#import RPi.GPIO as GPIO
import GPIO_mock as GPIO
import json
from app import conf as conf

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
        pinDao.add(conf["HOST"]+":"+iStr, mode, "-")

def getPins():
    return pinDao.getPins()

def updatePin(pinId, mode, value):
    pinIdSplited = pinId.split(":")
    pinNumber = int(pinIdSplited[1])
    
    pin = pinDao.getPin(pinId)
    
    #if isValid()
    if mode == "Disabled":
        #set Disabled
        if pin["mode"] == "Disabled":
            pass
        elif pin["mode"] == "Inactive":
            pinDao.update(pinId, mode, "-")
        elif pin["mode"] == "Output" or pin["mode"] == "Input" or pin["mode"] == "PWM":
            GPIO.cleanup(pinNumber)
            pinDao.update(pinId, mode, "-")
    elif mode == "Inactive":
        #set Inactive
        if pin["mode"] == "Disabled" or pin["mode"] == "Inactive":
            pass
        elif pin["mode"] == "Output" or pin["mode"] == "Input" or pin["mode"] == "PWM":
            GPIO.cleanup(pinNumber)
            pinDao.update(pinId, mode, "-")
    elif mode == "Output":
        #set Output
        if pin["mode"] == "Disabled":
            pass
        elif pin["mode"] == "Inactive" or pin["mode"] == "Input":
            if value == "On":
                GPIO.setup(pinNumber, GPIO.OUT)
                GPIO.output(pinNumber, GPIO.HIGH)
                pinDao.update(pinId, mode, value)
            elif value == "Off":
                GPIO.setup(pinNumber, GPIO.OUT)
                GPIO.output(pinNumber, GPIO.LOW)
                pinDao.update(pinId, mode, value)
        elif pin["mode"] == "Output":
            if value == "On":
                GPIO.output(pinNumber, GPIO.HIGH)
                pinDao.update(pinId, mode, value)
            elif value == "Off":
                GPIO.output(pinNumber, GPIO.LOW)
                pinDao.update(pinId, mode, value)
        elif pin["mode"] == "PWM":
            pass
    elif mode == "Input":
        #set Input
        if pin["mode"] == "Disabled":
            pass
        elif pin["mode"] == "Inactive" or pin["mode"] == "Output" or pin["mode"] == "PWM":
            GPIO.setup(pinNumber, GPIO.IN)
            value = GPIO.input(pinNumber)
            pinDao.update(pinId, mode, value)
        elif pin["mode"] == "Input":
            value = GPIO.input(pinNumber)
            pinDao.update(pinId, mode, value)
    elif mode == "PWM":
        #set PWM
        if pin["mode"] == "Disabled":
            pass
        elif pin["mode"] == "Inactive":
            pass
        elif pin["mode"] == "Output":
            pass
        elif pin["mode"] == "Input":
            pass
        elif pin["mode"] == "PWM":
            pass

def updateInputPins():
    pinData = getPins()
    for pinId in pinData:
        pin = pinData[pinId]
        
        if pin["mode"] == "Input":
            pinIdSplited = pinId.split(":")
            pinNumber = int(pinIdSplited[1])
            pin["value"] = GPIO.input(pinNumber)
            pinDao.update(pinId, pin["mode"], pin["value"])
            

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
    #print(getPins())
    #raise NotAllowedPinException
    #setOut('25')
    
    
    """print("Pin 13 enable: " + str(isValid(13)))
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
    #GPIO.setup(5, GPIO.OUT)"""
