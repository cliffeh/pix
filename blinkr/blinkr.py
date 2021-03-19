from flask import Flask, abort, jsonify, render_template, request

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

@app.route('/capabilities')
def capabilities():
    if not HAS_BLINKT:
        return jsonify(error="node does not have blinkt capabilities"), 404

    return {
        'blinkt': {
            'NUM_PIXELS': blinkt.num_pixels
        }
    }
