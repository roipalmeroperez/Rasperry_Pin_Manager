import time
import requests
import json
from app import conf as conf

def doWork():
	url = "http://localhost:" + str(conf["PORT"]) + "/pins/update"
	requests.post(url)

def timer():
	#time.sleep(4)
	prevTime = int(time.time()) + 1
	interval = conf["TIMER_INTERVAL_SECONDS"]

	while True:
		nextTime = prevTime + interval
		prevTime = nextTime
		
		doWork()
		time.sleep(nextTime - time.time())
