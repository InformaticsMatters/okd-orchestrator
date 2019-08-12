#!/bin/bash

flake8 *.py
flake8 utils/*.py
yamllint ansible
yamllint deployments
yamllint yacker
yamllint *.yml
