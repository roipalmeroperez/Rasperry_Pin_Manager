import time
import requests
import json
from app import conf as conf

url = "http://localhost:" + str(conf["PORT"]) + "/pins/updateInputs"

def timer():
	#time.sleep(4)
	prevTime = int(time.time()) + 1
	interval = conf["TIMER_INTERVAL_SECONDS"]

	while True:
		nextTime = prevTime + interval
		prevTime = nextTime
		
		# work
		requests.post(url)
		
		time.sleep(nextTime - time.time())
