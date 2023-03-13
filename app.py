import pins
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<pin>/<action>')
def pinset(pin, action):
    pin = int(pin)
    if ((pin < 1) or (pin > 40)):
        print('Pin out of range')
    elif not(pins.allowedPins[pin-1]):
        print('Not allowed pin')
    elif action == 'out':
        pins.setOut(pin)
    elif action == 'in':
        pins.setIn(pin)
    elif action == 'on':
        pins.on(pin)
    elif action == 'off':
        pins.off(pin)
    else:
        print('Pin: ' + str(pin) + ', action: ' + action)
        
    
    return render_template('index.html')
        


if __name__ == '__main__':
    pins.init()
    app.run(debug=True, host='0.0.0.0', port=8080)