#!/usr/bin/env bash
echo "mypy"
mypy --config-file=mypy.ini aio_sw

echo -e "\nflake8"
flake8 --config=.flake8 aio_sw

echo -e "\npylint"
pylint --rcfile=.pylintrc aio_sw
