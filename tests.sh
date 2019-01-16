#!/usr/bin/env bash
export FLASK_CONFIG=testing
export FLASK_APP=run.py

python -m unittest test_errors #3
python -m unittest test_views #8
python -m unittest test_models #24
python -m unittest test_integration #8
python -m unittest test_func #29
