import json, requests
import threading
from flask import Flask, render_template, abort, request

conf_file = open('./config.json')
conf = json.loads(conf_file.read())

import pins, devices, rules, timer


#import localPinsMock as localPins
import localPins

app = Flask(__name__)

# Server

@app.route('/')
def index():
    if conf["IS_SERVER"]:
        return render_template('index.html')
    else:
        return abort(403, "This host is not a server.")

@app.route('/devices', methods = ['POST', 'GET'])
def devicesWeb():
    
    if conf["IS_SERVER"]:
        if request.method == 'POST':
            
            if request.form['method'] == 'ADD':
                status = devices.addDevice(request.form['device'])
            elif request.form['method'] == 'DELETE':
                status = devices.removeDevice(request.form['device'])
            else:
                return abort(400)
            
            if status != 200 and status != 201:
                abort(status)
            
        
        return render_template('devices.html', devicesData = devices.getDevices())
    else:
        return abort(403, "This host is not a server.")
    

@app.route('/devices/<device>', methods = ['POST', 'GET'])
def devicesPinWeb(device):
    data = {}
    if request.method == 'POST':
        data = pins.updatePin(device, request.form['pin'], request.form['mode'], request.form['value'])

    else:
        data = pins.getPins(device)
    
    return render_template('pins.html', pinData = json.loads(data))

@app.route('/rules', methods = ['POST', 'GET'])
def rulesWeb():
    """if request.method == 'POST':
        rules.addRule(request.form)
    """
    return render_template('rules.html', rulesData = rules.getRules())

@app.route('/pins/update/<host>', methods = ['POST'])
def pinUpdateHost(host):
    #data = requests.text
    
    return {"status": "success"}, 200

# Host
serversList = []

@app.route('/master', methods = ['POST', 'DELETE', 'GET'])
def serversRoute():
    global serversList
    
    try:
        if request.method == 'GET':
            return {"master": devices.getMaster()}, 200
        elif request.method == 'POST':
            code = devices.addMaster(request.host)
            if code == 200 or code == 201:
                return {"status": "success"}, code
            else:
                return {"status": "fail"}, code
        elif request.method == 'DELETE':
            code = devices.deleteMaster(request.host)
            if code == 200:
                return {"status": "success"}, code
            else:
                return {"status": "fail"}, code
        else:
            return {"status": "fail"}, 500
    except:
        return {"status": "fail"}, 500

@app.route('/pins')
def pinWeb():
    return localPins.getPins(), 200

@app.route('/pins/update', methods = ['POST'])
def pinUpdate():
    localPins.updatePin(request.form['pin'], request.form['mode'], request.form['value'])
    return localPins.getPins(), 200

@app.route('/pins/updateInputs', methods = ['POST'])
def pinUpdateInputs():
    global serversList
    
    #data = localPins.updateInputPins()
    data = {"status": "success"}
    for server in serversList:
        url = "http://" + server + "/pins/update/" + conf["HOST"]
        requests.post(url, files = data)
        
    data = {"status": "success"}
    return data, 200




if __name__ == '__main__':
    localPins.loadPinData()
    timerThread = threading.Thread(target=timer.timer, daemon=True)
    timerThread.start()
    app.run(debug=True, host='0.0.0.0', port=conf["PORT"])    
