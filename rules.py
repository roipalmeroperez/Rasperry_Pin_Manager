from app import conf as conf

#ruleDao = __import__(conf["PIN_DAO_NAME"])

data = {}


def getRules():
    
    global data
    data["rule1"] = {"operand1":"pinId", "operation":"operation", "operand2":"value", "outputTarget":"pinId", "outputValue":"value", "ruleValue":False }
    
    return data


def addRule(operand1, operation, operand2, outputTarget, outputValue):
    pass

def deleteRule(ruleId):
    pass

def executeRules():
    pass

"""def addRule(form):
    #ruleDao(parameters)
    pass"""
