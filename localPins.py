import RPi.GPIO as GPIO
#import GPIO_mock as GPIO
import json, time

from app import conf as conf

pin_conf_file = open('./pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

localPins = {}
pwm = ""

def getPins():
	return localPins

def initPins():
	global localPins
	GPIO.setmode(GPIO.BOARD)
	
	for i in range(1, pin_conf['pinNumber'] + 1):
		iStr = str(i).zfill(2)
		if pin_conf[iStr]:
			mode = "Inactive"
		else:
			mode = "Disabled"
		localPins[iStr] = {"mode": mode, "value": ""}

def updatePin(pinId, mode, value):
	global localPins
	pin = localPins[pinId]
	pinNumber = int(pinId)
	
	if mode == "Disabled":
	#set Disabled
		if pin["mode"] == "Disabled":
			pass
		elif pin["mode"] == "Inactive":
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = ""
		elif pin["mode"] == "Output" or pin["mode"] == "Input" or pin["mode"] == "PWM":
			GPIO.cleanup(pinNumber)
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = ""
	elif mode == "Inactive":
	#set Inactive
		if pin["mode"] == "Disabled" or pin["mode"] == "Inactive":
			pass
		elif pin["mode"] == "Output" or pin["mode"] == "Input" or pin["mode"] == "PWM":
			GPIO.cleanup(pinNumber)
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = ""
	elif mode == "Output":
	#set Output
		if pin["mode"] == "Disabled":
			pass
		elif pin["mode"] == "Inactive" or pin["mode"] == "Input":
			if value == "On":
				GPIO.setup(pinNumber, GPIO.OUT)
				GPIO.output(pinNumber, GPIO.HIGH)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
			elif value == "Off":
				GPIO.setup(pinNumber, GPIO.OUT)
				GPIO.output(pinNumber, GPIO.LOW)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
		elif pin["mode"] == "Output":
			if value == "On":
				GPIO.output(pinNumber, GPIO.HIGH)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
			elif value == "Off":
				GPIO.output(pinNumber, GPIO.LOW)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
		elif pin["mode"] == "PWM":
			pass
	elif mode == "Input":
	#set Input
		if pin["mode"] == "Disabled":
			pass
		elif pin["mode"] == "Inactive" or pin["mode"] == "Output" or pin["mode"] == "PWM":
			GPIO.setup(pinNumber, GPIO.IN)
			localPins[pinId]["mode"] = mode
			localPins[pinId]["value"] = GPIO.input(pinNumber)
		elif pin["mode"] == "Input":
			localPins[pinId]["value"] = GPIO.input(pinNumber)
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
	
	return localPins

def updatePin2(pinId, mode, value):
	global localPins
	pin = localPins[pinId]
	pinNumber = int(pinId)
	global pwm
	
	if pin["mode"] == "Disabled":
		return localPins
	else:
		if mode in ["Disabled", "Inactive", "Input", "Output", "PWM"]:
			if pin["mode"] in ["Input", "Output", "PWM"]:
				GPIO.cleanup(pinNumber)
				time.sleep(0.2)
			if mode in ["Disabled", "Inactive"]:
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = ""
				return localPins
			elif mode == "Input":
				GPIO.setup(pinNumber, GPIO.IN)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = GPIO.input(pinNumber)
				return localPins
			elif mode == "Output":
				GPIO.setup(pinNumber, GPIO.OUT)
				if value == "On":
					GPIO.output(pinNumber, GPIO.HIGH)
					localPins[pinId]["mode"] = mode
					localPins[pinId]["value"] = value
					return localPins
				else:
					GPIO.output(pinNumber, GPIO.LOW)
					localPins[pinId]["mode"] = mode
					localPins[pinId]["value"] = "Off"
					return localPins
			elif mode == "PWM":
				GPIO.setup(pinNumber, GPIO.OUT)
				pwm = GPIO.PWM(pinNumber, 50)
				pwm.start(2)
				pwm.ChangeDutyCycle(float(value))
				time.sleep(0.2)
				pwm.stop()
				#GPIO.cleanup(pinNumber)
				localPins[pinId]["mode"] = mode
				localPins[pinId]["value"] = value
				return localPins
		
		# Not expected value
		return localPins
			
	

def updateInputPins():
	global localPins
	
	for pinId in localPins:
		if localPins[pinId]["mode"] == "Input":
			localPins[pinId]["value"] = GPIO.input(int(pinId))
	
	return localPins

def doWork():
	global pwm
	GPIO.setup(10, GPIO.OUT)
	pwm = GPIO.PWM(10, 50)
	pwm.start(2)
	pwm.ChangeDutyCycle(float("12"))
	time.sleep(0.2)
	GPIO.cleanup(10)
	
if __name__ == '__main__':
	initPins()
	print(getPins())
	#localPins["10"]["mode"] = "Input"
	#localPins["12"]["mode"] = "Input"
	#updateInputPins()
	#updatePin2("07", "Output", "On")
	updatePin2("10", "PWM", "2")
	"""GPIO.setup(10, GPIO.OUT)
	pwm = GPIO.PWM(10, 50)
	pwm.start(2)
	pwm.ChangeDutyCycle(float("4"))"""
	#doWork()
	#time.sleep(2)
	print(getPins())
	GPIO.cleanup()
	#GPIO.cleanup(10)
	
	
