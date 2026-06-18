import json, socket, datetime, mysql.connector, time, requests

def getGeneralConfiguration():
    conf_file = open('./config.json')
    conf = json.loads(conf_file.read())
    conf_file.close()
    return conf

def getPinConfiguration():
    pin_conf_file = open('./localPinsConfig.json')
    pin_conf = json.loads(pin_conf_file.read())
    pin_conf_file.close()
    return pin_conf

def getDatabaseConfiguration():
    conf = getGeneralConfiguration()
    configBD = {
        'user': conf["DATABASE_USER"],
        'password': conf["DATABASE_PASSWORD"],
        'host': conf["DATABASE_HOST"],
        'database': conf["DATABASE_DB"]
    }
    return configBD

def timer(url, interval):
	prevTime = int(time.time()) + 1
	
	while True:
		nextTime = prevTime + interval
		prevTime = nextTime
		
		# work
		requests.post(url)
		
		time.sleep(nextTime - time.time())

def validatePin(): 
    pass

def isBool(txt):
    if txt.lower() == "true":
        return (True, True)
    elif txt.lower() == "false":
        return (True, False)
    else: return (False, None)

def isPin(txt):
    txtSplited = txt.split(":")
    try: 
        host, portStr, pinStr = txtSplited 
        int(portStr) 
        int(pinStr) 
    except: 
        return (False, None)  
    return (True, txtSplited)

def isValidHost(address):
    txtSplited = address.split(":")
    try: 
        host, portStr = txtSplited 
        int(portStr)
    except: 
        return (False, None)  
    return (True, txtSplited)

def getIp():   
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def getDate():
    return datetime.datetime.now()

def getDateStr():
    x = datetime.datetime.now()
    dateStr = x.strftime("%Y") + x.strftime("%m") + x.strftime("%d")
    dateStr += x.strftime("%H") + x.strftime("%M") + x.strftime("%S")
    return dateStr

if __name__ == '__main__': 
    #print(isPin("localhost:4000:3")) 
    #print(isPin("localhost:4000:hola")) 
    #print(isPin("localhost:4000:3:hola")) print(isPin("True"))
    #print(getIp())
    #print(getDateStr())
    print(isValidHost("localhost:5000"))
    print(isValidHost("localhost:asd"))
    print(isValidHost("localhost:5000:20"))
    
