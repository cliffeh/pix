from flask import Flask, abort, jsonify, render_template, request
from functools import wraps

app = Flask(__name__)

HAS_BLINKT = False
try:
    import blinkt
    HAS_BLINKT = True
except (ImportError, RuntimeError):
    app.logger.warning('blinkt is not available on this machine, you will not be able to control (local) blinkenlights')

@app.route('/')
def index():
    pis = request.args.get('pis', '')
    return render_template('index.html', pis=pis.split(','))

### routes that require blinkt ###

def blinkt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not HAS_BLINKT:
            return jsonify(error="node does not have blinkt capabilities"), 404
        return f(*args, **kwargs)
    return decorated_function

@app.route('/capabilities')
@blinkt_required
def capabilities():
    return {
        'blinkt': {
            'NUM_PIXELS': blinkt.NUM_PIXELS
        }
    }

@app.route('/pixels')
@blinkt_required
def get_pixels():
    r = []
    for i in range(0, blinkt.NUM_PIXELS):
        r.append(blinkt.get_pixel(i)[:3])
    return jsonify(r)

@app.route('/pixels/<int:id>')
@blinkt_required
def get_pixel(id=None):
    return jsonify(blinkt.get_pixel(id)[:3])

@app.route('/pixels/<int:id>/<int:r>/<int:g>/<int:b>', methods = ['POST'])
@blinkt_required
def set_pixel(id=None, r=0, g=0, b=0):
    blinkt.set_pixel(id, r, g, b)
    blinkt.show()
    return jsonify(blinkt.get_pixel(id)[:3])
