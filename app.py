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

@app.route('/devices', methods = ['GET'])
def devicesWeb():
    
    if conf["IS_SERVER"]:
        return render_template('devices.html', devicesData = devices.getDevices())
    else:
        return abort(403, "This host is not a server.")

"""Cambiar métodos addDevice y removeDevice (no deben gestionar peticiones)"""
@app.route('/devices', methods = ['POST'])
def addDeleteDevices():
    
    if conf["IS_SERVER"]:
        if request.form['method'] == 'ADD':
            status = devices.addDevice(request.form['device'])
        elif request.form['method'] == 'DELETE':
            status = devices.deleteDevice(request.form['device'])
        else:
            return abort(400)
        
        if status != 200 and status != 201:
            abort(status)
            
        
        return render_template('devices.html', devicesData = devices.getDevices())
    else:
        return abort(403, "This host is not a server.")

"""Dividir en 2 métodos"""
@app.route('/devices/<device>', methods = ['POST', 'GET'])
def devicesPinWeb(device):
    data = {}
    if request.method == 'POST':
        data = pins.updatePin(device, request.form['pin'], request.form['mode'], request.form['value'])
        #return data

    else:
        data = pins.getPins(device)
    
    return render_template('pins.html', pinData = json.loads(data))

@app.route('/rules', methods = ['GET'])
def rulesWeb():
    return render_template('rules.html', rulesData = rules.getRules())

@app.route('/rules', methods = ['POST'])
def addDeleteRules():
    if request.form['operand1'] != "":
        rules.addRule(request.form['operand1'], request.form['operation'], request.form['operand2'], request.form['outputTarget'], request.form['outputValue'])
    if request.form['deletedRuleId'] != "":
        rules.deleteRule(request.form['deletedRuleId'])
    return render_template('rules.html', rulesData = rules.getRules())

@app.route('/pins/update/<host>', methods = ['POST'])
def pinUpdateHost(host):
    #falta registrar los cambios
    #data = requests.text
    #print(data)
    #pins.updatePins(host, requests.text)
    data = json.loads(request.get_json())
    pins.updatePins(host, data)
    
    return {"status": "success"}, 200

# Host

@app.route('/master', methods = ['GET'])
def getMaster():
    return {"master": devices.getMaster()}, 200

@app.route('/master', methods = ['POST'])
def addMaster():
    master = devices.getMaster()
    if master == request.host:
        return {"status": "success"}, 200
    elif master == "":
        devices.addMaster(request.host)
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
    timerThread = threading.Thread(target=timer.timer, daemon=True)
    timerThread.start()
    app.run(debug=True, host='0.0.0.0', port=conf["PORT"])    
