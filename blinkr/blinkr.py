from flask import Flask, render_template, request

app = Flask(__name__)

try:
    import blinkt
except ImportError:
    app.logger.warning('blinkt is not available on this machine, you will not be able to control (local) blinkenlights')

@app.route('/')
def index():
    pis = request.args.get('pis', '')
    return render_template('index.html', pis=pis.split(','))
