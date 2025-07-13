"""
This module contains the code of the server and the responses of the
http petitions.
"""

# External modules
import json, requests, datetime
import threading
from flask import Flask, render_template, abort, request, send_from_directory

# Configuration
conf_file = open('./config.json')
conf = json.loads(conf_file.read())

# Our modules
import pins, devices, rules, utils

app = Flask(__name__)
ownIp = utils.getIp()

# Server

# Index

@app.route('/')
# This method displays the main website
def indexWeb():
    return render_template('base.html')

# Devices

@app.route('/devices', methods = ['GET'])
# This method displays the devices website
def devicesWeb():
    return render_template('devices.html', devicesData = devices.getDevices())

@app.route('/devices', methods = ['POST'])
# This method manages the posts launched by the devices website
def addDeleteDevices():
    devicesList = devices.getDevices()
    device = request.form['device']
    
    if request.form['method'] == 'ADD':
        if device in devicesList:
            return render_template('devices.html', devicesData = devicesList)
        
        else:
            try:
                url = "http://" + device + ":" + str(conf["SLAVE_PORT"]) + "/master"
                dataForm = {'newMaster': (None, ownIp)}
                response = requests.post(url, files = dataForm)
            except:
                return abort(404)
                
            url = "http://" + device + ":" + str(conf["SLAVE_PORT"]) + "/pins"
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
                url = "http://" + device + ":" + str(conf["SLAVE_PORT"]) + "/master"
                response = requests.delete(url)
            except:
                abort(404)
    
    else:
        return abort(405)
    
    return render_template('devices.html', devicesData = devicesList)


# Pins

@app.route('/devices/<device>', methods = ['GET'])
# This method displays pins of a particular device
def devicesPinWeb(device):
    return render_template('pins.html', pinData = pins.getPins(device))

@app.route('/devices/<device>', methods = ['POST'])
# This method manages the posts launched by the pins website and allows the pin value modification
def devicesUpdatePins(device):
    dataForm = {'pin': (None, request.form['pin']), 'mode': (None, request.form['mode']), 'value': (None, request.form['value'])}
    response = requests.post("http://" + device + ":" + str(conf["SLAVE_PORT"]) + "/pins", files = dataForm)
    data = json.loads(response.text)
    pins.updatePins(device, data)
    rules.executeRules()
    
    return render_template('pins.html', pinData = data)

# Rules

@app.route('/rules', methods = ['GET'])
def rulesWeb():
    return render_template('rules.html', rulesData = rules.getRules())

@app.route('/rules', methods = ['POST'])
def addDeleteRules():
    if request.form['ruleId'] != "":
        # falta validar los datos
        rules.addRule(request.form['ruleId'], request.form['operand1'], request.form['operation'], request.form['operand2'], request.form['outputTarget'], request.form['outputValue'])
        # rules.executeRules()
    if request.form['deletedRuleId'] != "":
        rules.deleteRule(request.form['deletedRuleId'])
    return render_template('rules.html', rulesData = rules.getRules())

# Pins update

@app.route('/pins/update/<host>', methods = ['POST'])
def pinUpdateHost(host):
    
    data = json.loads(request.get_json())
    pins.updatePins(host, data)
    rules.executeRules()
    
    return {"status": "success"}, 200

# Data control

@app.route('/pinsData', methods = ['GET'])
def pinsData():
    return pins.getPinData(), 200



# Main program

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=conf["MANAGER_PORT"])    
