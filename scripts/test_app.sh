#!/usr/bin/env bash

set -e

# run black - make sure everyone uses same python style
black --skip-string-normalization --line-length 120 --check django_excel
black --skip-string-normalization --line-length 120 --check manage.py
black --skip-string-normalization --line-length 120 --check core/
black --skip-string-normalization --line-length 120 --check tests/

# run isort for import structure checkup with black profile
isort --atomic --profile black -c django_excel
isort --atomic --profile black -c manage.py
isort --atomic --profile black -c core/
isort --atomic --profile black -c tests/

# run mypy
mypy core/

# run bandit - A security linter from OpenStack Security
bandit -r core/

# python static analysis
prospector  --profile=.prospector.yml --path=core --ignore-patterns=static
prospector  --profile=.prospector.yml --path=tests --ignore-patterns=static
