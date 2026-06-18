"""
This module contains the DAO code that allows the system pin 
information to be stored in a SQL Database.
"""
import utils, mysql.connector

configBD = utils.getDatabaseConfiguration()

# Methods
def getPinData():
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	cursor.execute("SELECT pin_ip, pin_number, description, pin_mode, pin_value FROM pins;")
	result = cursor.fetchall()
	data = {}
	for x in result:
		data[x[0]][x[1]] = {"description": x[2], "pin_mode": x[3], "pin_value": x[4]}
	cursor.close()
	cnx.close()
	return data

def getPins(host):
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	sql = "SELECT pin_number, description, pin_mode, pin_value FROM pins WHERE pin_ip = %s"
	val = (host, )
	cursor.execute(sql, val)
	result = cursor.fetchall()
	data = {}
	for x in result:
		data[x[0]] = {"description": x[1], "pin_mode": x[2], "pin_value": x[3]}
	cursor.close()
	cnx.close()
	return data

def getPin(host, pin):
	global pinList
	return pinList[host][pin]

def addPins(host, pinData):
	global pinList
	pinList[host] = pinData

def deletePins(host):
	global pinList
	pinList.pop(host)

def update(host, pinId, mode, value):
	global pinList
	pinList[host][pinId] = {
		"mode": mode,
		"value": value
		}

def updatePins(host, pinData):
	global pinList
	pinList[host] = pinData
