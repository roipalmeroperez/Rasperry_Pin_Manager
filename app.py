"""
This module contains the code of the server and the responses of the
http petitions.
"""

import json, requests
import threading
from flask import Flask, render_template, abort, request

conf_file = open('./config.json')
conf = json.loads(conf_file.read())

import pins, devices, rules, timer

import localPins

app = Flask(__name__)

# Server

@app.route('/')
def index():
    if conf["IS_SERVER"]:
        return render_template('index.html')
    else:
        return abort(403, "This host is not a server.")

@app.route('/devices', methods = ['GET'])
def devicesWeb():
    
    if conf["IS_SERVER"]:
        return render_template('devices.html', devicesData = devices.getDevices())
    else:
        return abort(403, "This host is not a server.")

@app.route('/devices', methods = ['POST'])
def addDeleteDevices():
    
    if conf["IS_SERVER"]:
        devicesList = devices.getDevices()
        device = request.form['device']
        
        if request.form['method'] == 'ADD':
            if device in devicesList:
                return render_template('devices.html', devicesData = devicesList)
            
            else:
                try:
                    url = "http://" + device + "/master"
                    dataForm = {'newMaster': (None, conf["HOST"] + ":" + str(conf["PORT"]))}
                    response = requests.post(url, files = dataForm)
                except:
                    return abort(404)
                    
                url = "http://" + device + "/pins"
                response = requests.get(url)
                data = json.loads(response.text)
                pins.addPins(device, data)
                
                devicesList = devices.addDevice(device)
            
        elif request.form['method'] == 'DELETE':
            if not(device in devicesList):
                return abort(404)
            
            else:
                devicesList = devices.deleteDevice(device)
                pins.deletePins(device)
                try:
                    url = "http://" + device + "/master"
                    response = requests.delete(url)
                except:
                    abort(404)
        
        else:
            return abort(400)
        
        return render_template('devices.html', devicesData = devicesList)
    else:
        return abort(403, "This host is not a server.")

@app.route('/devices/<device>', methods = ['GET'])
def devicesPinWeb(device):
    if conf["IS_SERVER"]:
        data = pins.getPins(device)
        
        return render_template('pins.html', pinData = data)
    else:
        return abort(403, "This host is not a server.")

@app.route('/devices/<device>', methods = ['POST'])
def devicesUpdatePins(device):
    if conf["IS_SERVER"]:
        dataForm = {'pin': (None, request.form['pin']), 'mode': (None, request.form['mode']), 'value': (None, request.form['value'])}
        response = requests.post("http://" + device + "/pins/update", files = dataForm)
        data = json.loads(response.text)
        pins.updatePins(device, data)
        
        return render_template('pins.html', pinData = data)
    else:
        return abort(403, "This host is not a server.")

@app.route('/rules', methods = ['GET'])
def rulesWeb():
    return render_template('rules.html', rulesData = rules.getRules())

@app.route('/rules', methods = ['POST'])
def addDeleteRules():
    if request.form['operand1'] != "":
        rules.addRule(request.form['ruleId'], request.form['operand1'], request.form['operation'], request.form['operand2'], request.form['outputTarget'], request.form['outputValue'])
    if request.form['deletedRuleId'] != "":
        rules.deleteRule(request.form['deletedRuleId'])
    return render_template('rules.html', rulesData = rules.getRules())

@app.route('/pins/update/<host>', methods = ['POST'])
def pinUpdateHost(host):
    data = json.loads(request.get_json())
    pins.updatePins(host, data)
    
    return {"status": "success"}, 200
   
@app.route('/pinsData', methods = ['GET'])
def pinsData():
    return pins.getPinData(), 200

# Host

@app.route('/master', methods = ['GET'])
def getMaster():
    return {"master": devices.getMaster()}, 200

@app.route('/master', methods = ['POST'])
def addMaster():
    master = devices.getMaster()
    newMaster = request.form['newMaster']
    if master == newMaster:
        return {"status": "success"}, 200
    elif master == "":
        devices.addMaster(newMaster)
        return {"status": "success"}, 201
    else:
        return {"status": "fail"}, 403

@app.route('/master', methods = ['DELETE'])
def deleteMaster():
    devices.deleteMaster()
    return {"status": "success"}, 200

@app.route('/pins', methods = ['GET'])
def pinWeb():
    return localPins.getPins(), 200

@app.route('/pins/update', methods = ['POST'])
def pinUpdate():
    data = localPins.updatePin(request.form['pin'], request.form['mode'], request.form['value'])
    return data, 200

@app.route('/pins/updateInputs', methods = ['POST'])
def pinUpdateInputs():
    pinData = localPins.updateInputPins()
    
    master = devices.getMaster()
    if master != "":
        url = "http://" + master + "/pins/update/" + conf["HOST"] + ":" + str(conf["PORT"])
        requests.post(url, json=json.dumps(pinData))
    
    data = {"status": "success"}
    return data, 200

if __name__ == '__main__':
    localPins.loadPinData()
    timerThread = threading.Thread(target=timer.timer, args=(conf["PORT"], conf["TIMER_INTERVAL_SECONDS"]), daemon=True)
    timerThread.start()
    app.run(debug=True, host='0.0.0.0', port=conf["PORT"])    
