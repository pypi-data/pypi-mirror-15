#!/bin/bash
coverage run --branch --source philutils --omit=tests/*.py,setup.py -m unittest discover .
coverage report --show-missing
coverage html
