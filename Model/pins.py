import RPi.GPIO as GPIO
import json

pin_conf_file = open('./Model/pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

class NotAllowedPinException(Exception):
    "Exception raised for illegal pin assignment"
    
    def __init__(self):
        self.message = "Illegal pin assignment"
        super().__init__(self.message)

def init():
    GPIO.setmode(GPIO.BOARD)

def setOut(pin):
    if pin_conf[pin]:
        GPIO.setup(int(pin), GPIO.OUT)
    else:
        raise NotAllowedPinException

def setIn(pin):
    if pin_conf[pin]:
        GPIO.setup(int(pin), GPIO.IN)
    else:
        raise NotAllowedPinException

def on(pin):
    GPIO.output(pin, GPIO.HIGH)
    
def off(pin):
    GPIO.output(pin, GPIO.LOW)



if __name__ == '__main__':
    # Tests
    pin_conf_file = open('pin_config.json')
    pin_conf = json.loads(pin_conf_file.read())
    init()
    #raise NotAllowedPinException
    #setOut('25')
    #print(pin_conf['25'])
    #on(16)
    GPIO.setup(5, GPIO.OUT)