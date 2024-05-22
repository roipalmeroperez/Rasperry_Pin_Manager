from app import conf as conf

#ruleDao = __import__(conf["PIN_DAO_NAME"])

data = {}


def getRules():
    
    global data
    data["rule1"] = {"inputId":"pinId", "operation":"operation", "valueInput":"value", "outputId":"pinId", "outputValue":"value"}
    
    return data
"""
<td><input type = "text" name = "inputId" /></td>
               <td><select name="operation" id="operation">
                  <option value="greater than">greater than</option>
                  <option value="less than">less than</option>
                  <option value="equals">equals</option>
                  <option value="not equals">not equals</option>
               </select></td>
               <td><input type = "text" name = "valueInput" /></td>
               <td><input type = "text" name = "outputId" /></td>
               <td><input type = "text" name = "outputValue" /><
"""

def addRule(inputId, operation, valueInput, outputId, outputValue):
    pass

def deleteRule(ruleId):
    pass

def executeRules():
    pass

"""def addRule(form):
    #ruleDao(parameters)
    pass"""
