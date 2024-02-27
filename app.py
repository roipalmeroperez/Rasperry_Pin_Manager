import json, requests
import threading
from flask import Flask, render_template, abort, request

conf_file = open('./config.json')
conf = json.loads(conf_file.read())

import pins, devicesDaoRam, rules, timer

app = Flask(__name__)

@app.route('/')
def index():
    if conf["IS_MASTER"]:
        return render_template('index.html')
    else:
        return abort(403, "This host is not a master.")

@app.route('/pins')
def pinWeb():
    return pins.getPins(), 200

@app.route('/pins/update', methods = ['POST'])
def pinUpdate():
    pins.updateInputPins()
    # modificar para envió desde el esclavo al maestro
    data = {"status": "success"}
    return data, 200

@app.route('/pins/update/<host>', methods = ['POST', 'GET'])
def pinUpdateHost():
    
    return data, 200

@app.route('/devices', methods = ['POST', 'GET'])
def devicesWeb():
    if request.method == 'POST':
        if request.form['method'] == 'ADD':
            devicesDaoRam.addDevice(request.form['device'])
        elif request.form['method'] == 'DELETE':
            devicesDaoRam.removeDevice(request.form['device'])
    
    return render_template('devices.html', devicesData = devicesDaoRam.getDevices())

@app.route('/devices/<device>', methods = ['POST', 'GET'])
def devicesPinWeb(device):
    if request.method == 'POST':
        pins.updatePin(request.form['pin'], request.form['mode'], request.form['value'])
        
        #return {"status": "success"}, 200

    url ="http://" + device + ":" + str(conf["PORT"]) + "/pins"
    response = requests.get(url)
    
    return render_template('pins.html', pinData = json.loads(response.text))

@app.route('/rules', methods = ['POST', 'GET'])
def rulesWeb():
    """if request.method == 'POST':
        rules.addRule(request.form)
    """
    return render_template('rules.html', rulesData = rules.getRules())

if __name__ == '__main__':
    pins.init()
    timerThread = threading.Thread(target=timer.timer, daemon=True)
    timerThread.start()
    app.run(debug=True, host='0.0.0.0', port=conf["PORT"])    
