"""
This module contains the code to handle the rules of the master.
"""
# Imports
# import datetime
import requests, json
import utils, pins

# Configuration
conf_file = open('./config.json')
conf = json.loads(conf_file.read())

# DAOs
rulesDao = __import__(conf["RULES_DAO_NAME"])

# Methods
"""def getRuleId():
    x = datetime.datetime.now()
    ruleId = x.strftime("%Y") + x.strftime("%m") + x.strftime("%d")
    ruleId += x.strftime("%H") + x.strftime("%M") + x.strftime("%S")
    return ruleId"""

def isRule(ruleId):
    return rulesDao.isRule(ruleId)

def validateOperand(operand):
    pass
    #if isRule(operand):
    #    return True

def validateOperation(operator):
    pass

def getOperandValue(operand):
    global rulesData
    if isRule(operand):
        return rulesData[operand]["ruleValue"]
    itIsAPin, pin = utils.isPin(operand)
    if itIsAPin:
        host, port, pinNumber = pin
        pin = pins.getPin(host + ":" + port, pinNumber)
        return pin["value"]
    # is a value
    return operand

def getRules():
    return rulesDao.getRules()

def addRule(ruleId, operand1, operation, operand2, outputTarget, outputValue):
    # validación de datos en app.py
    rulesDao.addRule(ruleId, operand1, operation, operand2, outputTarget, outputValue)
    return 201

def deleteRule(ruleId):
    if isRule(ruleId):
        rulesDao.deleteRule(ruleId)
        return 200
    else:
        return 404

def executeRule(rule):
    
    print("Rule " + rule["ruleId"] + " executed.")
    return True
    
    #try:
    """revisar datos de entrada (si son pines, reglas o valores)"""
    opnd1 = getOperandValue(rule["operand1"])
    opnd2 = getOperandValue(rule["operand2"])
    
    """hacer la operación"""
    if rule["operation"] == "equals":
        rule["ruleValue"] = (opnd1 == opnd2)
    elif rule["operation"] == "not equals":
        rule["ruleValue"] = (opnd1 != opnd2)
    elif rule["operation"] == "greater than":
        rule["ruleValue"] = (opnd1 > opnd2)
    elif rule["operation"] == "less than":
        rule["ruleValue"] = (opnd1 < opnd2)
    elif rule["operation"] == "AND":
        rule["ruleValue"] = (opnd1 and opnd2)
    elif rule["operation"] == "OR":
        rule["ruleValue"] = (opnd1 or opnd2)
    
    """revisar qué hacer con el resultado (dar valor a la regla y puede que cambiar un pin)"""
    if rule["ruleValue"]:
        itIsAPin, data = utils.isPin(rule["outputTarget"])
        if itIsAPin:
            host, port, pinNumber = data
            pin = pins.getPin(host + ":" + port, pinNumber)
            # enviar petición POST
            dataForm = {'pin': (None, pinNumber), 'mode': (None, pin["mode"], ), 'value': (None, rule["outputValue"])}
            requests.post("http://" + host + ":" + port + "/pins", files = dataForm)
            pins.updatePin(host + ":" + port, pinNumber, pin["mode"], rule["outputValue"])
    #except:
    #    pass
    

def executeRules():
    rulesData = rulesDao.getRules()
    
    for rule in rulesData.values():
        executeRule(rule)


