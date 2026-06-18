"""
This module contains the code of the server and the responses of the
http petitions.
"""

# External modules
import json, requests, threading
from flask import Flask, render_template, abort, request, send_from_directory, send_file

# Our modules
import localPins, camera, utils

# Configuration
conf = utils.getGeneralConfiguration()

app = Flask(__name__)
master = ""
ownIp = utils.getIp()

# Index

@app.route('/')
# This method displays the main website
def indexWeb():
    return render_template('indexSlave.html', pinData = localPins.getPins())

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
        return {"status": "success", "ip": ownIp}, 200
    elif master == "":
        master = newMaster
        return {"status": "success", "ip": ownIp}, 201
    else:
        return {"status": "fail"}, 403

@app.route('/master', methods = ['DELETE'])
def deleteMaster():
    global master
    master = ""
    return {"status": "success"}, 200

# Devices

@app.route('/alive', methods = ['GET'])
def devicesAlive():
    return {"status": "success"}, 200

# Local pins

@app.route('/pins', methods = ['GET'])
def pinData():
    return localPins.getPins(), 200

@app.route('/pins', methods = ['POST'])
def pinUpdate():
    global master
    origin = request.remote_addr
    if origin == master:
        data = localPins.updatePin(request.form['pin'], request.form['description'], request.form['mode'], request.form['value'])
        return data, 200
    else:
        return abort(403)

@app.route('/updateInputs', methods = ['POST'])
def pinUpdateInputs():
    global master
    pinData = localPins.updateInputPins()
    
    if master != "":
        url = "http://" + master + ":" + str(conf["MANAGER_PORT"]) + "/pins/update/" + ownIp
        requests.post(url, json=json.dumps(pinData))
    
    return {"status": "success"}, 200

# Camera

@app.route('/camera', methods = ['GET'])
def takeFoto():
    pictureName = utils.getDateStr() + '.jpg'
    camera.takeFoto('./' + conf["PICTURES_ROUTE"], pictureName)
    
    return send_file('./' + conf["PICTURES_ROUTE"] + pictureName, mimetype='image/jpg')


# Main program

if __name__ == '__main__':
    
    localPins.loadPins()
    url = "http://localhost:" + str(conf["SLAVE_PORT"]) + "/updateInputs"
    inputUpdaterThread = threading.Thread(target=utils.timer, args=(url, conf["INPUT_INTERVAL_SECONDS"]), daemon=True)
    inputUpdaterThread.start()
    app.run(debug=True, host='0.0.0.0', port=conf["SLAVE_PORT"])    
