"""
This module contains the code to handle the rules of the master.
"""

from app import conf as conf
import datetime

#ruleDao = __import__(conf["PIN_DAO_NAME"])

data = {}
data["rule1"] = {"operand1":"pinId", "operation":"operation", 
"operand2":"value", "outputTarget":"pinId", "outputValue":"value", 
"ruleValue":False }

def getRuleId():
    x = datetime.datetime.now()
    ruleId = x.strftime("%Y") + x.strftime("%m") + x.strftime("%d")
    ruleId += x.strftime("%H") + x.strftime("%M") + x.strftime("%S")
    return ruleId
    

def getRules():
    
    global data
    return data

def addRule(ruleId, operand1, operation, operand2, outputTarget, outputValue):
    global data
    
    data[ruleId] = {"operand1":operand1, "operation":operation, 
    "operand2":operand2, "outputTarget":outputTarget, 
    "outputValue":outputValue, "ruleValue":False }

"""def addRule(operand1, operation, operand2, outputTarget, outputValue):
    global data
    ruleId = getRuleId()
    addRule(ruleId, operand1, operation, operand2, outputTarget, outputValue)"""

def deleteRule(ruleId):
    global data
    data.pop(ruleId)

def executeRules():
    pass
