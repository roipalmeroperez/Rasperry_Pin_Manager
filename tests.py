import requests

urlServer ="http://192.168.1.10:8080"

def addDevice(device):
	dataForm = {'method': (None, 'ADD'), 'device': (None, device),}
	response = requests.post(urlServer + "/devices", files = dataForm)

def deleteDevice(device):
	dataForm = {'method': (None, 'DELETE'), 'device': (None, device),}
	response = requests.post(urlServer + "/devices", files = dataForm)

def addGetAndRemoveDeviceTest():
	response = requests.get(urlServer + "/devices")
	if '192.168.1.10' in response.text:
		return False
	
	addDevice('192.168.1.10:8080')
	
	response = requests.get(urlServer + "/devices")
	if not('192.168.1.10:8080' in response.text):
		return False
	
	deleteDevice('192.168.1.10:8080')
	
	response = requests.get(urlServer + "/devices")
	if '192.168.1.10' in response.text:
		return False
	
	return True

def updatePinTest():
	dataForm = {'pin': (None, '10'), 'mode': (None, 'Output'), 'value': (None, 'On')}
	response = requests.post(urlServer + "/pins/update", files = dataForm)

if __name__ == '__main__':
	print('Test name: ' + 'addGetAndRemoveDeviceTest' + '; Result: ' + str(addGetAndRemoveDeviceTest()))
	"""response = requests.get(urlServer + "/pins")
	print(response.text)
	updatePinTest()
	response = requests.get(urlServer + "/pins")
	print(response.text)"""
	
