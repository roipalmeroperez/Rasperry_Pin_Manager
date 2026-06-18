import requests, sys
import utils

#urlMaster = "http://192.168.1.132:8080"
#host = '192.168.1.132'
conf = utils.getGeneralConfiguration()



def deleteBlankSpaces(text):
	s = text.replace(" ", "")
	s = s.replace("\n", "")
	return s

def addDevice(urlMaster, device):
	dataForm = {'method': (None, 'ADD'), 'device': (None, device), 'description': (None, ''), }
	requests.post(urlMaster + "/devices", files = dataForm)

def deleteDevice(urlMaster, device):
	dataForm = {'method': (None, 'DELETE'), 'device': (None, device), }
	requests.post(urlMaster + "/devices", files = dataForm)

def addAndRemoveDeviceTest(urlMaster, host):
	print('Starting test: addGetAndRemoveDeviceTest...')
	
	response = requests.get(urlMaster + "/devices")
	if host in response.text:
		print('Result: Fail. Host is added.')
		return False
	
	dataForm = {'method': (None, 'ADD'), 'device': (None, host), 'description': (None, host + ' description'), }
	addResponse = requests.post(urlMaster + "/devices", files = dataForm)
	if addResponse.status_code != 201:
		print('Code: ' + str(addResponse.status_code))
		print('Result: Fail. Error with status code adding host.')
		return False
	
	response = requests.get(urlMaster + "/devices")
	if not(host in response.text):
		print('Result: Fail. Error adding host.')
		return False
	
	dataForm = {'method': (None, 'DELETE'), 'device': (None, host), }
	deleteResponse = requests.post(urlMaster + "/devices", files = dataForm)
	if deleteResponse.status_code != 200:
		print('Result: Fail. Error with status code deleting host.')
		return False
	
	response = requests.get(urlMaster + "/devices")
	if host in response.text:
		print('Result: Fail. Error deleting host.')
		return False
	
	print('Result: Success.')
	return True

def addInvalidDeviceTest(urlMaster, invalidHost):
	print('Starting test: addInvalidDeviceTest...')
	
	dataForm = {'method': (None, 'ADD'), 'device': (None, invalidHost), 'description': (None, invalidHost + ' description'), }
	addResponse = requests.post(urlMaster + "/devices", files = dataForm)
	if addResponse.status_code != 404:
		print('Result: Fail. Error with status code adding host.')
		return False
	
	print('Result: Success.')
	return True

def addAddedDeviceTest(urlMaster, host):
	print('Starting test: addAddedDeviceTest...')
	
	addDevice(urlMaster, host)
	
	dataForm = {'method': (None, 'ADD'), 'device': (None, host), 'description': (None, host + ' description'), }
	addResponse = requests.post(urlMaster + "/devices", files = dataForm)
	if addResponse.status_code != 200:
		print('Result: Fail. Error with status code adding added host.')
		return False
	
	deleteDevice(urlMaster, host)
	
	print('Result: Success.')
	return True

def removeInvalidDeviceTest(urlMaster, host):
	print('Starting test: removeInvalidDeviceTest...')
	
	dataForm = {'method': (None, 'DELETE'), 'device': (None, host), }
	deleteResponse = requests.post(urlMaster + "/devices", files = dataForm)
	if deleteResponse.status_code != 404:
		print('Result: Fail. Error with status code deleting host.')
		return False
	
	print('Result: Success.')
	return True

def getPinsHostTest(urlMaster, host):
	print('Starting test: getPinsHostTest...')
	
	addDevice(urlMaster, host)
	
	response = requests.get(urlMaster + "/devices/" + host)
	if response.status_code != 200:
		print('Result: Fail. Error with status code.')
		return False
	
	deleteDevice(urlMaster, host)
	
	print('Result: Success.')
	return True

def getPinsInvalidHostTest(urlMaster, host):
	print('Starting test: getPinsInvalidHostTest...')
	
	response = requests.get(urlMaster + "/devices/" + host)
	if response.status_code != 404:
		print('Result: Fail. Error with status code.')
		return False
	
	print('Result: Success.')
	return True

def updatePinValuesTest(urlMaster, host):
	print('Starting test: updatePinTest...')
	
	# Adding the slave
	addDevice(urlMaster, host)
	url = urlMaster + "/devices/" + host
	
	# Check Disabled
	
	dataForm = {'pin': (None, '06'), 'description': (None, 'checking_Disabled'), 'mode': (None, 'Disabled'), 'value': (None, '1')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>06</td><td>checking_Disabled</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The description should change and value should be empty.')
		return False
	
	dataForm = {'pin': (None, '06'), 'description': (None, 'inactive'), 'mode': (None, 'Inactive'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>06</td><td>checking_Disabled</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change to Inactive mode.')
		return False
	
	dataForm = {'pin': (None, '06'), 'description': (None, 'output off'), 'mode': (None, 'Output'), 'value': (None, '0')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>06</td><td>checking_Disabled</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change to Output mode and low value.')
		return False
	
	dataForm = {'pin': (None, '06'), 'description': (None, 'output on'), 'mode': (None, 'Output'), 'value': (None, '1')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>06</td><td>checking_Disabled</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change to Output mode and high value.')
		return False
	
	dataForm = {'pin': (None, '06'), 'description': (None, 'input'), 'mode': (None, 'Input'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>06</td><td>checking_Disabled</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change to Input mode.')
		return False
	
	dataForm = {'pin': (None, '06'), 'description': (None, 'pwm'), 'mode': (None, 'PWM'), 'value': (None, '5')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>06</td><td>checking_Disabled</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change to PWM mode.')
		return False
	
	# Check Inactive
	
	dataForm = {'pin': (None, '08'), 'description': (None, 'checking_Inactive'), 'mode': (None, 'Inactive'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>08</td><td>checking_Inactive</td><td>Inactive</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The description in Inactive mode should change.')
		return False
	
	# Check Output
	
	dataForm = {'pin': (None, '10'), 'description': (None, 'checking_Output'), 'mode': (None, 'Output'), 'value': (None, '0')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>10</td><td>checking_Output</td><td>Output</td><td>0</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change to Output mode and low value.')
		return False
	
	dataForm = {'pin': (None, '10'), 'description': (None, 'checking_Output'), 'mode': (None, 'Output'), 'value': (None, '1')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>10</td><td>checking_Output</td><td>Output</td><td>1</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change to Output mode and high value.')
		return False
	
	dataForm = {'pin': (None, '10'), 'description': (None, 'checking_Output'), 'mode': (None, 'Output'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>10</td><td>checking_Output</td><td>Output</td><td>0</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change to Output mode and low value by default.')
		return False
	
	dataForm = {'pin': (None, '10'), 'description': (None, 'checking_Output'), 'mode': (None, 'Input'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>10</td><td>checking_Output</td><td>Output</td><td>0</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change from Output to Input.')
		return False
	
	dataForm = {'pin': (None, '10'), 'description': (None, 'checking_Output'), 'mode': (None, 'PWM'), 'value': (None, '5')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>10</td><td>checking_Output</td><td>Output</td><td>0</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change from Output to PWM.')
		return False
	
	dataForm = {'pin': (None, '10'), 'description': (None, 'checking_Output'), 'mode': (None, 'Inactive'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>10</td><td>checking_Output</td><td>Inactive</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change from Output to Inactive.')
		return False
	
	dataForm = {'pin': (None, '10'), 'description': (None, ''), 'mode': (None, 'Output'), 'value': (None, '0')}
	requests.post(url, files = dataForm)
	dataForm = {'pin': (None, '10'), 'description': (None, 'checking_Output'), 'mode': (None, 'Disabled'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>10</td><td>checking_Output</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change from Output to Disabled.')
		return False
	
	# Check Input
	dataForm = {'pin': (None, '16'), 'description': (None, 'checking_Input'), 'mode': (None, 'Input'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>16</td><td>checking_Input</td><td>Input</td>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change to Input mode.')
		return False
	
	dataForm = {'pin': (None, '16'), 'description': (None, 'checking_Input'), 'mode': (None, 'Output'), 'value': (None, '0')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>16</td><td>checking_Input</td><td>Input</td>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change from Input to Output.')
		return False
	
	dataForm = {'pin': (None, '16'), 'description': (None, 'checking_Input'), 'mode': (None, 'PWM'), 'value': (None, '5')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>16</td><td>checking_Input</td><td>Input</td>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change from Output to Inactive.')
		return False
	
	dataForm = {'pin': (None, '16'), 'description': (None, 'checking_Input'), 'mode': (None, 'Inactive'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>16</td><td>checking_Input</td><td>Inactive</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change from Input to Inactive.')
		return False
	
	dataForm = {'pin': (None, '16'), 'description': (None, ''), 'mode': (None, 'Input'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	dataForm = {'pin': (None, '16'), 'description': (None, 'checking_Input'), 'mode': (None, 'Disabled'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>16</td><td>checking_Input</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change from Input to Disabled.')
		return False
	
	# Check PWM
	dataForm = {'pin': (None, '22'), 'description': (None, 'checking_PWM'), 'mode': (None, 'PWM'), 'value': (None, '5.5')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>22</td><td>checking_PWM</td><td>PWM</td><td>5.5</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change to PWM mode.')
		return False
	
	dataForm = {'pin': (None, '22'), 'description': (None, 'checking_PWM'), 'mode': (None, 'PWM'), 'value': (None, '10.5')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>22</td><td>checking_PWM</td><td>PWM</td><td>10.5</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The value should change in PWM mode.')
		return False
	
	dataForm = {'pin': (None, '22'), 'description': (None, 'checking_PWM'), 'mode': (None, 'Output'), 'value': (None, '0')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>22</td><td>checking_PWM</td><td>PWM</td><td>10.5</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change from PWM to Output mode.')
		return False
	
	dataForm = {'pin': (None, '22'), 'description': (None, 'checking_PWM'), 'mode': (None, 'Input'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>22</td><td>checking_PWM</td><td>PWM</td><td>10.5</td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should not change from PWM to Input mode.')
		return False
	
	dataForm = {'pin': (None, '22'), 'description': (None, 'checking_PWM'), 'mode': (None, 'Inactive'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>22</td><td>checking_PWM</td><td>Inactive</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change to from PWM to Inactive mode.')
		return False
	
	dataForm = {'pin': (None, '22'), 'description': (None, 'checking_PWM'), 'mode': (None, 'PWM'), 'value': (None, '10.5')}
	requests.post(url, files = dataForm)
	dataForm = {'pin': (None, '22'), 'description': (None, 'checking_PWM'), 'mode': (None, 'Disabled'), 'value': (None, '')}
	requests.post(url, files = dataForm)
	response = requests.get(urlMaster + "/devices/" + host)
	pin = "<tr><td>22</td><td>checking_PWM</td><td>Disabled</td><td></td></tr>"
	if not(pin in deleteBlankSpaces(response.text)):
		print('Result: Fail. The mode should change from PWM to Disabled mode.')
		return False
	
	
	
	# Restore pin data
	
	
	deleteDevice(urlMaster, host)
	print('Result: Success.')
	return True

def updateInvalidPinTest(urlMaster, host):
	print('Starting test: updateInvalidPinTest...')
	
	# Adding the slave
	addDevice(urlMaster, host)
	url = urlMaster + "/devices/" + host
	
	dataForm = {'pin': (None, '-1'), 'description': (None, ''), 'mode': (None, 'Output'), 'value': (None, '1')}
	response = requests.post(url, files = dataForm)
	if response.status_code != 400:
		print('Result: Fail. The request must fail.')
		return False
	
	deleteDevice(urlMaster, host)
	print('Result: Success.')
	return True
	
def updateInvalidPinArgumentsTest(urlMaster, host):
	pass

def updatePinNoMasterHostTest(urlMaster, host):
	print('Starting test: updatePinNoMasterHostTest...')
	
	url = "http://" + host + ":" + str(conf["SLAVE_PORT"]) + "/pins"
	
	dataForm = {'pin': (None, '10'), 'description': (None, ''), 'mode': (None, 'Output'), 'value': (None, '1')}
	response = requests.post(url, files = dataForm)
	if response.status_code != 403:
		print('Result: Fail. The request must fail.')
		return False
	
	print('Result: Success.')
	return True

def addAndRemoveRuleTest(urlMaster, host):
	print('Starting test: addAndRemoveRuleTest...')
	
	# Adding the slave
	addDevice(urlMaster, host)
	url = urlMaster + "/rules"
	
	dataForm = {'method': (None, 'ADD'), 'ruleId': (None, 'rule1'), 'operand1': (None, host + ':10'), 
		'operation': (None, 'equals'), 'operand2': (None, '1'), 'outputTarget': (None, host + ':12'),
		'outputValue': (None, '1')}
	response = requests.post(url, files = dataForm)
	if response.status_code != 201:
		print('Result: Fail. The adding request code is not as expected.')
		return False
	
	response = requests.get(url)
	if not('rule1' in response.text):
		print('Result: Fail. Error adding rule.')
		return False
	
	dataForm = {'method': (None, 'DELETE'), 'ruleId': (None, 'rule1')}
	response = requests.post(url, files = dataForm)
	if response.status_code != 200:
		print('Result: Fail. The deleting request code is not as expected.')
		return False
	
	response = requests.get(url)
	if ('rule1' in response.text):
		print('Result: Fail. Error deleting rule.')
		return False
	
	deleteDevice(urlMaster, host)
	print('Result: Success.')
	return True

def addInvalidRule():
	pass

def removeNonExistingRuleTest(urlMaster):
	print('Starting test: removeNonExistingRuleTest...')
	
	url = urlMaster + "/rules"
	dataForm = {'method': (None, 'DELETE'), 'ruleId': (None, 'rule5')}
	response = requests.post(url, files = dataForm)
	if response.status_code != 404:
		print('Result: Fail. The deleting request code is not as expected.')
		return False
	
	print('Result: Success.')
	return True

def executeRulesTest():
	pass

if __name__ == '__main__':
	if len(sys.argv) == 3:
		urlMaster = sys.argv[1]
		host = sys.argv[2]
		addAndRemoveDeviceTest(urlMaster, host)
		addInvalidDeviceTest(urlMaster, '8.8.8.8')
		addAddedDeviceTest(urlMaster, host)
		removeInvalidDeviceTest(urlMaster, host)
		getPinsHostTest(urlMaster, host)
		getPinsInvalidHostTest(urlMaster, host)
		#updatePinValuesTest(urlMaster, host)
		updateInvalidPinTest(urlMaster, host)
		updateInvalidPinArgumentsTest(urlMaster, host)
		updatePinNoMasterHostTest(urlMaster, host)
		addAndRemoveRuleTest(urlMaster, host)
		addInvalidRule()
		removeNonExistingRuleTest(urlMaster)
		executeRulesTest()
		
	else:
		print('Invalid number of arguments.')
