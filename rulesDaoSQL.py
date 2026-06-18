"""
This module contains the code to handle the rules of the master.
"""

# Global variables

configBD = utils.getDatabaseConfiguration()

# Methods

def getRules():
    cnx = mysql.connector.connect(**configBD)
    cursor = cnx.cursor()
    cursor.execute("SELECT id, operand1, rule_op, operand2, output_target, output_value, rule_value FROM rules;")
    result = cursor.fetchall()
    data = {}
    for x in result:
	    data[x[0]] = {"ruleId": x[0], "operand1": x[1], "operation": x[2], "operand2": x[3], "outputTarget": x[4], "outputValue": x[5], "ruleValue": x[6]}
    cursor.close()
    cnx.close()
    return data

def getRule(ruleId):
    cnx = mysql.connector.connect(**configBD)
    cursor = cnx.cursor()
    sql = "SELECT id, operand1, rule_op, operand2, output_target, output_value, rule_value FROM rules WHERE id = %s"
    val = (ruleId)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    data = {}
    for x in result:
	    data[x[0]] = {"ruleId": x[0], "operand1": x[1], "operation": x[2], "operand2": x[3], "outputTarget": x[4], "outputValue": x[5], "ruleValue": x[6]}
    cursor.close()
    cnx.close()
    return data

def isRule(ruleId):
    cnx = mysql.connector.connect(**configBD)
    cursor = cnx.cursor()
    sql = "SELECT * FROM rules WHERE id = %s"
    val = (deviceIp, )
    cursor.execute(sql, val)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return len(result) == 1

def addRule(ruleId, operand1, operation, operand2, outputTarget, outputValue):
    global rulesData
    rulesData[ruleId] = {"ruleId": ruleId, "operand1":operand1,
    "operation":operation, "operand2":operand2, "outputTarget":outputTarget, 
    "outputValue":outputValue, "ruleValue":False }
    cnx = mysql.connector.connect(**configBD)
    cursor = cnx.cursor()
    sql = "INSERT INTO rules (id, operand1, rule_op, operand2, output_target, output_value, rule_value) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (ruleId, operand1, operation, operand2, outputTarget, outputValue, False)
    cursor.execute(sql, val)
    cnx.commit()

def deleteRule(ruleId):
    cnx = mysql.connector.connect(**configBD)
    cursor = cnx.cursor()
    sql = "DELETE FROM rules WHERE id = %s"
    val = (ruleId, )
    cursor.execute(sql, val)
    cnx.commit()
