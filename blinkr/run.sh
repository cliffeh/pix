#!/bin/bash

BLINKR_HOME="$(dirname $0)"
echo "Using BLINKR_HOME=${BLINKR_HOME}"

source "${BLINKR_HOME}/venv/bin/activate"
export FLASK_APP="${BLINKR_HOME}/blinkr.py"
flask run --reload --extra-files templates/index.html
