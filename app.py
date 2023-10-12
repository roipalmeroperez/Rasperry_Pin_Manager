import json, requests
import threading
from flask import Flask, render_template, abort, request

conf_file = open('./config.json')
conf = json.loads(conf_file.read())

import pins, devicesDaoRam, rules, timer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forbidden')
def forbidenWeb():
    return abort(403, "Custom message.")

@app.route('/error')
def errorWeb():
    return abort(500)

@app.route('/pins')
def pinWeb():
    return pins.getPins(), 200

"""@app.route('/pins/<pin>/<action>')
def pinset(pin, action):
    if action == 'out':
        pins.setOut(pin)
    elif action == 'in':
        pins.setIn(pin)
    elif action == 'on':
        pins.on(pin)
    elif action == 'off':
        pins.off(pin)
    elif action == 'clear':
        pins.clear(pin)
    else:
        print('Pin: ' + str(pin) + ', action: ' + action)
    
    return render_template('pins.html', pinData = pins.getPins())
"""        
@app.route('/rules', methods = ['POST', 'GET'])
def rulesWeb():
    """if request.method == 'POST':
        rules.addRule(request.form)
    """
    return render_template('rules.html', rulesData = rules.getRules())

@app.route('/devices', methods = ['POST', 'GET'])
def devicesWeb():
    if request.method == 'POST':
        devicesDaoRam.addDevice(request.form['device'])
    
    return render_template('devices.html', devicesData = devicesDaoRam.getDevices())

@app.route('/devices/<device>', methods = ['POST', 'GET'])
def devicesPinWeb(device):
    if request.method == 'POST':
        pins.updatePin(request.form['pin'], request.form['mode'], request.form['value'])
    url ="http://" + device + ":8080/pins"
    response = requests.get(url)
    
    return render_template('pins.html', pinData = json.loads(response.text))

@app.route('/pins/update', methods = ['POST'])
def pinUpdate():
    pins.updateInputPins()
    data = {"status": "success"}
    return data, 200

if __name__ == '__main__':
    pins.init()
    timerThread = threading.Thread(target=timer.timer, daemon=True)
    timerThread.start()
    app.run(debug=True, host='0.0.0.0', port=8080)    
