#! /bin/bash

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

./venv/bin/python -m flask run --cert adhoc
