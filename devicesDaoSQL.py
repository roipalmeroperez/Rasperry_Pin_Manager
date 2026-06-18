import utils, mysql.connector

configBD = utils.getDatabaseConfiguration()

def getDevices():
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	cursor.execute("SELECT ip, description, last_update, alive FROM devices;")
	result = cursor.fetchall()
	data = {}
	for x in result:
		data[x[0]] = {"deviceIp": x[0], "description": x[1], "lastUpdate": x[2], "alive": x[3]}
	cursor.close()
	cnx.close()
	return data

def getDevice(deviceIp):
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	sql = "SELECT ip, description, last_update, alive FROM devices WHERE ip = %s"
	val = (deviceIp)
	cursor.execute(sql, val)
	result = cursor.fetchall()
	data = {}
	for x in result:
		data[x[0]] = {"deviceIp": x[0], "description": x[1], "lastUpdate": x[2], "alive": x[3]}
	cursor.close()
	cnx.close()
	return data

def isAddedDevice(deviceIp):
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	sql = "SELECT * FROM devices WHERE ip = %s"
	val = (deviceIp, )
	cursor.execute(sql, val)
	result = cursor.fetchall()
	cursor.close()
	cnx.close()
	return len(result) == 1
	
def addDevice(deviceIp, description, lastUpdate, alive):
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	sql = "INSERT INTO devices (ip, description, last_update, alive) VALUES (%s, %s, %s, %s)"
	val = (deviceIp, description, lastUpdate, alive)
	cursor.execute(sql, val)
	cnx.commit()

def updateDevice(deviceIp, description, lastUpdate, alive):
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	sql = "UPDATE devices SET description = %s, last_update = %s, alive = %s WHERE ip = %s"
	val = (description, lastUpdate, alive, deviceIp)
	cursor.execute(sql, val)
	cnx.commit()

def deleteDevice(deviceIp):
	cnx = mysql.connector.connect(**configBD)
	cursor = cnx.cursor()
	sql = "DELETE FROM devices WHERE ip = %s"
	val = (deviceIp, )
	cursor.execute(sql, val)
	cnx.commit()
