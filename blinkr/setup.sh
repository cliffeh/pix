#!/bin/bash

set -e

BLINKR_HOME="$(dirname $0)"
echo "Using BLINKR_HOME=${BLINKR_HOME}"

python3 -m venv "${BLINKR_HOME}/venv"
source "${BLINKR_HOME}/venv/bin/activate"
pip install -r "${BLINKR_HOME}/requirements.txt"

