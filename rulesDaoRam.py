"""
This module contains the code to handle the rules of the master.
"""

# Global variables

rulesData = {}

# Methods

def getRules():
    global rulesData
    return rulesData

def getRule(ruleId):
    global rulesData
    return rulesData[ruleId]

def isRule(ruleId):
    global rulesData
    return ruleId in rulesData

def addRule(ruleId, operand1, operation, operand2, outputTarget, outputValue):
    global rulesData
    rulesData[ruleId] = {"ruleId": ruleId, "operand1":operand1,
    "operation":operation, "operand2":operand2, "outputTarget":outputTarget, 
    "outputValue":outputValue, "ruleValue":False }

def deleteRule(ruleId):
    global rulesData
    rulesData.pop(ruleId)
