#! /bin/bash

export FLASK_CONFIG=default
export FLASK_APP=main.py
export FLASK_ENV=development
export FLASK_DEBUG=1

./venv/bin/python -m flask run --cert adhoc
