import time
import requests

def timer(port, interval):
	url = "http://localhost:" + str(port) + "/updateInputs"
	prevTime = int(time.time()) + 1
	
	while True:
		nextTime = prevTime + interval
		prevTime = nextTime
		
		# work
		requests.post(url)
		
		time.sleep(nextTime - time.time())
