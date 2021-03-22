from flask import Flask, abort, jsonify, render_template, request
from functools import wraps
import requests

# TODO externalize into config
PIS=['pi4','pi3','pi2','pi1']
PORT=5000

app = Flask(__name__)

HAS_BLINKT = False
try:
    import blinkt
    HAS_BLINKT = True
except (ImportError, RuntimeError):
    app.logger.warning('blinkt is not available on this machine, you will not be able to control (local) blinkenlights')

@app.route('/')
def index():
    return render_template('index.html')

### routes that forward requests on to other pis ###

@app.route('/pis')
def all_pis():
    pis = []
    for pi in PIS:
        r = requests.get(f'http://{pi}:{PORT}/pixels')
        # TODO handle errors
        pis.append({ 'name': pi, 'pixels': r.json() })
    return jsonify(pis)

def valid_pi_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if kwargs['pi'] not in PIS:
            return jsonify(error="node does not support talking to this pi"), 400
        return f(*args, **kwargs)
    return decorated_function

@app.route('/pis/<pi>', methods = ['GET', 'POST'])
@valid_pi_required
def get_or_set_pi(pi=None):
    r = requests.get(f'http://{pi}:{PORT}/pixels')
    # TODO handle errors
    return r.text, r.status_code

@app.route('/pis/<pi>/pixels/<int:id>/<int:r>/<int:g>/<int:b>', methods = ['POST'])
@valid_pi_required
def get_or_set_pi_pixels(pi=None, id=None, r=None, g=None, b=None):
    r = requests.post(f'http://{pi}:{PORT}/pixels/{id}/{r}/{g}/{b}')
    # TODO handle errors
    return r.text, r.status_code

### routes that require blinkt locally ###

def blinkt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not HAS_BLINKT:
            return jsonify(error="node does not have blinkt capabilities"), 404
        return f(*args, **kwargs)
    return decorated_function

@app.route('/pixels', methods = ['GET', 'POST'])
@blinkt_required
def all_pixels():
    if request.method == 'POST':
        blinkt.set_all(0, 0, 0)
        blinkt.show()
    r = []
    for i in range(0, blinkt.NUM_PIXELS):
        r.append(blinkt.get_pixel(i)[:3])
    return jsonify(r)

@app.route('/pixels/<int:id>', methods = ['GET', 'POST'])
@blinkt_required
def get_or_set_pixel(id=None):
    if request.method == 'POST':
        blinkt.set_pixel(id, 0, 0, 0)
        blinkt.show()
    return jsonify(blinkt.get_pixel(id)[:3])

@app.route('/pixels/<int:id>/<int:r>/<int:g>/<int:b>', methods = ['POST'])
@blinkt_required
def set_pixel(id=None, r=0, g=0, b=0):
    blinkt.set_pixel(id, r, g, b)
    blinkt.show()
    return jsonify(blinkt.get_pixel(id)[:3])
