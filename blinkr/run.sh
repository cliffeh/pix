#!/bin/bash

BLINKR_HOME="$(dirname $0)"
echo "Using BLINKR_HOME=${BLINKR_HOME}"

source "${BLINKR_HOME}/venv/bin/activate"
export FLASK_APP="${BLINKR_HOME}/blinkr.py"
# TODO make 0.0.0.0 optional
flask run --host 0.0.0.0 --reload --extra-files templates/index.html
