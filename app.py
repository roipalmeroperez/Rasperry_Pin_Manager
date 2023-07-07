import pins as pins
from flask import Flask, render_template, abort, request


app = Flask(__name__)
rules = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forbidden')
def forbidenWeb():
    return abort(403, "Custom message.")

@app.route('/error')
def errorWeb():
    return abort(500)

@app.route('/pins', methods = ['POST', 'GET'])
def pinweb():
    if request.method == 'POST':
        pins.updatePin('pin' + request.form['pin'], request.form['pin'], 
            request.form['mode'], request.form['value'])
    
    return render_template('pins.html', pinData = pins.getPins())
    

@app.route('/pins/<pin>/<action>')
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
        
    templateData = pins.pinList
    return render_template('pins.html', pinData = pins.getPins())
        
@app.route('/rules', methods = ['POST', 'GET'])
def rulesWeb():
    if request.method == 'POST':
        rules[len(rules)] = {
            'name': request.form['name'],
            'password': request.form['password']
            }
    
    return render_template('rules.html', rulesData = rules)

if __name__ == '__main__':
    pins.init()
    app.run(debug=True, host='0.0.0.0', port=8080)    
