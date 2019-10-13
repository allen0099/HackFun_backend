#! /bin/bash

export FLASK_CONFIG=test
export FLASK_APP=main.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask shell
