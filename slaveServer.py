"""
This module contains the code of the server and the responses of the
http petitions.
"""

# External modules
import json, requests, datetime
import threading
from flask import Flask, render_template, abort, request, send_from_directory

# Our modules
import localPins, camera, timer, utils

# Configuration
conf_file = open('./config.json')
conf = json.loads(conf_file.read())
app = Flask(__name__)
master = ""
ownIp = utils.getIp()



# Index

@app.route('/')
# This method displays the main website
def indexWeb():
    print(request.remote_addr)
    return render_template('indexSlave.html', pinData = localPins.getPins())

# Host

# Master manage

@app.route('/master', methods = ['GET'])
def getMaster():
    global master
    
    return {"master": master}, 200

@app.route('/master', methods = ['POST'])
def addMaster():
    global master
    
    newMaster = request.remote_addr
    if master == newMaster:
        return {"status": "success"}, 200
    elif master == "":
        master = newMaster
        return {"status": "success"}, 201
    else:
        return {"status": "fail"}, 403

@app.route('/master', methods = ['DELETE'])
def deleteMaster():
    global master
    master = ""
    return {"status": "success"}, 200

# Local pins

@app.route('/pins', methods = ['GET'])
def pinWeb():
    return localPins.getPins(), 200

@app.route('/pins', methods = ['POST'])
def pinUpdate():
    data = localPins.updatePin(request.form['pin'], request.form['mode'], request.form['value'])
    return data, 200

# Local pins update

@app.route('/updateInputs', methods = ['POST'])
def pinUpdateInputs():
    global master
    pinData = localPins.updateInputPins()
    
    if master != "":
        url = "http://" + master + ":" + str(conf["MANAGER_PORT"]) + "/pins/update/" + ownIp
        requests.post(url, json=json.dumps(pinData))
    
    data = {"status": "success"}
    return data, 200

# Camera

@app.route('/camera', methods = ['GET'])
def takeFoto():
    pictureName = utils.getDateStr() + '.jpg'
    camera.takeFoto('./' + conf["PICTURES_ROUTE"], pictureName)
    
    return send_from_directory(conf["PICTURES_ROUTE"], pictureName)


# Main program

if __name__ == '__main__':
    
    localPins.loadPinData()
    timerThread = threading.Thread(target=timer.timer, args=(conf["SLAVE_PORT"], conf["TIMER_INTERVAL_SECONDS"]), daemon=True)
    timerThread.start()
    app.run(debug=True, host='0.0.0.0', port=conf["SLAVE_PORT"])    
