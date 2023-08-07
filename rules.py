from app import conf as conf

#ruleDao = __import__(conf["PIN_DAO_NAME"])

data = {}


def getRules():
    
    global data
    data["rule1"] = {"name":"name", "password":"password"}
    
    return data

"""def addRule(form):
    #ruleDao(parameters)
    pass"""
