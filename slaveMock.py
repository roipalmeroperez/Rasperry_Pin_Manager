import json, requests
import threading
from flask import Flask, render_template, abort, request
import app as appServer
import sys

conf_file = open('./config.json')
conf = json.loads(conf_file.read())

import pins, devices, rules, timer


import localPinsMock

app = Flask(__name__)


# Server

@app.route('/')
def index():
    data = localPinsMock.getPins()
    
    return render_template('pins.html', pinData = data)

@app.route('/', methods = ['POST'])
def changePins():
    data = localPinsMock.updatePin(request.form['pin'], request.form['mode'], request.form['value'])
    return render_template('pins.html', pinData = data)

# Host


@app.route('/master', methods = ['GET'])
def getMaster():
    return appServer.getMaster()

@app.route('/master', methods = ['POST'])
def addMaster():
    return appServer.addMaster()

@app.route('/master', methods = ['DELETE'])
def deleteMaster():
    return appServer.deleteMaster()

@app.route('/pins')
def pinWeb():
    return localPinsMock.getPins(), 200

@app.route('/pins/update', methods = ['POST'])
def pinUpdate():
    data = localPinsMock.updatePin(request.form['pin'], request.form['mode'], request.form['value'])
    return data, 200

@app.route('/pins/updateInputs', methods = ['POST'])
def pinUpdateInputs():
    pinData = localPinsMock.updateInputPins()
    
    master = devices.getMaster()
    if master != "":
        url = "http://" + master + "/pins/update/" + conf["HOST"] + ":" + sys.argv[1]
        requests.post(url, json=json.dumps(pinData))
    
    data = {"status": "success"}
    return data, 200




if __name__ == '__main__':
    portNumber = int(sys.argv[1])
    interval = int(sys.argv[2])
    localPinsMock.loadPinData()
    timerThread = threading.Thread(target=timer.timer, args=(portNumber, interval), daemon=True)
    timerThread.start()
    app.run(debug=True, host='0.0.0.0', port=portNumber)
    
