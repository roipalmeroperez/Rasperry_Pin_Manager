OUT = "out"
IN = "in"
HIGH = "high"
LOW = "low"
BOARD = "board"

def setmode(mode):
	print("Set mode: " + mode)

def setup(pin, value):
	print("Pin: " + str(pin) + ", value: " + value)

def output(pin, value):
	print("Pin: " + str(pin) + ", value: " + value)

def input(pin):
	return 0
