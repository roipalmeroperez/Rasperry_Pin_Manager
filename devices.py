from app import conf as conf
import requests

devicesDao = __import__(conf["DEVICES_DAO_NAME"])

def getDevices():
	return devicesDao.getDevices()

def addDevice(device):
	if devicesDao.existsDevice(device):
		return 403
	try:
		url = "http://" + device + "/servers"
		response = requests.post(url)
	except:
		return 404
	try:
		devicesDao.addDevice(device)
	except:
		return 500
	
	return 201
		
	
def removeDevice(device):
	if not(devicesDao.existsDevice(device)):
		return 403
	try:
		devicesDao.removeDevice(device)
		url = "http://" + device + "/servers"
		response = requests.delete(url)
	except:
		return 404
	
	return 200
	
