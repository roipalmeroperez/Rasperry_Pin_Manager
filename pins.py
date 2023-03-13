import RPi.GPIO as GPIO

allowedPins = [False, False, True, False, True, False, True, True, False, True,
               True, True, True, False, True, True, False, True, True, False,
               True, True, True, True, False, True, True, True, True, False,
               True, True, True, False, True, True, True, True, False, True]

def init():
    GPIO.setmode(GPIO.BOARD)

def setOut(pin):
    GPIO.setup(pin, GPIO.OUT)

def setIn(pin):
    GPIO.setup(pin, GPIO.IN)

def on(pin):
    GPIO.output(pin, GPIO.HIGH)
    
def off(pin):
    GPIO.output(pin, GPIO.LOW)
