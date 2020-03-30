#! /bin/bash

source settings.sh

cd ../

./venv/bin/python -m flask run --cert adhoc
