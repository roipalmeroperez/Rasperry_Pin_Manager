"""
This module contains the code to handle the rules of the master.
"""
# Imports
# import datetime
import requests
import utils, pins

# Import configuration
from app import conf as conf


# DAOs
#ruleDao = __import__(conf["RULE_DAO_NAME"])

# Global variables
rulesData = {}
#rulesData["rule1"] = {"operand1":"pinId", "operation":"operation", 
#"operand2":"value", "outputTarget":"pinId", "outputValue":"value", 
#"ruleValue":False }

# Methods
"""def getRuleId():
    x = datetime.datetime.now()
    ruleId = x.strftime("%Y") + x.strftime("%m") + x.strftime("%d")
    ruleId += x.strftime("%H") + x.strftime("%M") + x.strftime("%S")
    return ruleId"""

def isRule(ruleId):
    global rulesData
    return ruleId in rulesData

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
    global rulesData
    return rulesData

def addRule(ruleId, operand1, operation, operand2, outputTarget, outputValue):
    global rulesData
    # validación de datos en app.py
    rulesData[ruleId] = {"operand1":operand1, "operation":operation, 
    "operand2":operand2, "outputTarget":outputTarget, 
    "outputValue":outputValue, "ruleValue":False }

def deleteRule(ruleId):
    global rulesData
    rulesData.pop(ruleId)

def executeRule(ruleId):
    
    print("Rule " + ruleId + " executed.")
    #return True
    
    global rulesData
    rule = rulesData[ruleId]
    
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
    global rulesData
    for ruleId in rulesData:
        executeRule(ruleId)


