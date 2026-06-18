"""
This module contains the code of the server and the responses of the
http petitions.
"""

# External modules
import json, requests, io
import threading
from flask import Flask, render_template, abort, request, send_from_directory, send_file, jsonify
import mysql.connector

from flask_mysqldb import MySQL
#from flask_sqlalchemy import SQLAlchemy

# Our modules
import pins, devices, rules, utils

# Configuration
app = Flask(__name__)
ownIp = utils.getIp()
conf = utils.getGeneralConfiguration()
configBD = utils.getDatabaseConfiguration()


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
    if request.form['method'] == 'ADD':
        device = request.form['device']
        code = devices.addDevice(request.form['device'], request.form['description'])
        #code = devices.addDevice(device, "description")
        if not code in [200, 201]:
            return abort(code)
    elif request.form['method'] == 'DELETE':
        device = request.form['device']
        code = devices.deleteDevice(device)
        if code != 200:
            return abort(code)
    else:
        return abort(405)
    
    return render_template('devices.html', devicesData = devices.getDevices()), code

@app.route('/devices/alive', methods = ['POST'])
# This method displays the devices website
def aliveManager():
    devicesList = devices.getDevices()
    for device in devicesList:
        try:
            # Actualiza la información del device
            response = requests.get("http://" + device + ":" + str(conf["SLAVE_PORT"]) + "/alive")
            devices.updateDevice(devicesList[device]["deviceIp"], devicesList[device]["description"], devicesList[device]["lastUpdate"], True)
        except:
            # Marca el device como offline
            devices.updateDevice(devicesList[device]["deviceIp"], devicesList[device]["description"], devicesList[device]["lastUpdate"], False)

    return {"status": "success"}, 200

# Pins

@app.route('/devices/<device>', methods = ['GET'])
# This method displays pins of a particular device
def devicesPinWeb(device):
    if devices.isAddedDevice(device):
        return render_template('pins.html', pinData = pins.getPins(device))
    else:
        abort(404)

@app.route('/devices/<device>', methods = ['POST'])
# This method manages the posts launched by the pins website and allows the pin value modification
def devicesUpdatePins(device):
    if not pins.isPin(device, request.form['pin']):
        abort(400)
    dataForm = {'pin': (None, request.form['pin']), 'description': (None, request.form['description']), 'mode': (None, request.form['mode']), 'value': (None, request.form['value'])}
    response = requests.post("http://" + device + ":" + str(conf["SLAVE_PORT"]) + "/pins", files = dataForm)
    if response.status_code != 200:
        abort(response.status_code)
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
    if request.form['method'] == "ADD":
        # falta validar los datos
        code = rules.addRule(request.form['ruleId'], request.form['operand1'], request.form['operation'], request.form['operand2'], request.form['outputTarget'], request.form['outputValue'])
        # rules.executeRules()
    elif request.form['method'] == "DELETE":
        code = rules.deleteRule(request.form['ruleId'])
    else:
        return abort(405)
    
    return render_template('rules.html', rulesData = rules.getRules()), code

# Pins update

@app.route('/pins/update/<host>', methods = ['POST'])
def pinUpdateHost(host):
    
    data = json.loads(request.get_json())
    pins.updatePins(host, data)
    device = devices.getDevice(host)
    devices.updateDevice(device["deviceIp"], device["description"], utils.getDate(), device["alive"])
    rules.executeRules()
    
    return {"status": "success"}, 200

# Camera
@app.route('/devices/<host>/takeFoto', methods = ['GET'])
def fotoManager(host):
    """response = requests.get("http://" + host + ":" + str(conf["SLAVE_PORT"]) + "/camera", stream=True, timeout=10)
    return response, 200
    
    try:
        response = requests.get("http://" + host + ":" + str(conf["SLAVE_PORT"]) + "/camera", stream=True, timeout=5)
        
        # Si el otro host responde con un error (ej. 404), detenemos el proceso
        if response.status_code != 200:
            return "No se pudo encontrar la imagen en el servidor remoto.", response.status_code

        # 4. Leer el contenido de la imagen en un buffer de memoria (BytesIO)
        imagen_en_memoria = io.BytesIO(response.content)
        
        # Obtener el tipo de contenido (ej. 'image/jpeg' o 'image/png')
        content_type = response.headers.get('Content-Type', 'image/jpg')

        # 5. Enviar el archivo directamente al navegador del usuario
        return send_file(imagen_en_memoria, mimetype=content_type)

    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión (host apagado, timeout, etc.)
        return f"Error de conexión con el host remoto: {e}", 500
    """
    try:
        # Hacemos la petición GET al Servidor 2 pasando el nombre del archivo
        response = requests.get("http://" + host + ":" + str(conf["SLAVE_PORT"]) + "/camera", stream=True, timeout=10)
        
        # Si el Servidor 2 responde con un error (404, 400, etc.), se lo notificamos al usuario
        if response.status_code != 200:
            return f"Error en el servidor de imágenes: {response.text}", response.status_code

        # Pasamos los bytes de la respuesta a un buffer en la memoria RAM
        imagen_en_memoria = io.BytesIO(response.content)
        
        # Obtenemos el tipo de imagen (image/jpeg, image/png) que nos envió el Servidor 2
        tipo_contenido = response.headers.get('Content-Type', 'image/jpg')

        # Enviamos la imagen directamente al navegador del usuario
        return send_file(imagen_en_memoria, mimetype='image/jpg')

    except requests.exceptions.RequestException as e:
        return f"No se pudo conectar con el servidor de almacenamiento: {e}", 500
    

# Data control

@app.route('/pinsData', methods = ['GET'])
def pinsData():
    return pins.getPinData(), 200

@app.route('/db')
def datos():
    cnx = mysql.connector.connect(**configBD)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users;")
    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(data)

# Main program

if __name__ == '__main__':
    url = "http://localhost:" + str(conf["MANAGER_PORT"]) + "/devices/alive"
    aliveManagerThread = threading.Thread(target=utils.timer, args=(url, conf["INPUT_INTERVAL_SECONDS"]), daemon=True)
    aliveManagerThread.start()
    app.run(debug=True, host='0.0.0.0', port=conf["MANAGER_PORT"])
