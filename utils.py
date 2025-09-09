import socket, datetime, mysql.connector

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

def getIp():   
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def getDateStr():
    x = datetime.datetime.now()
    dateStr = x.strftime("%Y") + x.strftime("%m") + x.strftime("%d")
    dateStr += x.strftime("%H") + x.strftime("%M") + x.strftime("%S")
    return dateStr

if __name__ == '__main__': 
    #print(isPin("localhost:4000:3")) 
    #print(isPin("localhost:4000:hola")) 
    #print(isPin("localhost:4000:3:hola")) print(isPin("True"))
    print(getIp())
    print(getDateStr())
