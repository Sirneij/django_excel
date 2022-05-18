# django_excel

![main](https://github.com/Sirneij/django_excel/actions/workflows/django.yml/badge.svg?branch=main)
![Issues](https://img.shields.io/github/issues/Sirneij/django_excel)
![Forks](https://img.shields.io/github/forks/Sirneij/django_excel)
![Stars](https://img.shields.io/github/stars/Sirneij/django_excel)
![License](https://img.shields.io/github/license/Sirneij/django_excel)

This repository accompanies [this tutorial][1] on dev.to. It has been deployed to heroku and can be accessed live via [this link][2].

## Run locally

It can be run locally by creating a virtual environment using any of `venv`, `poetry`, `virtualenv`, and `pipenv`. I used `virtualenv` while developing the app. Having created the virtual environment, activate it and install the project's dependencies by issuing the following command in your terminal:

```bash
(env) sirneij@pop-os ~/D/P/T/django_excel (main)> pip install -r requirements.txt
```

Then, `migrate` the database:

```bash
(env) sirneij@pop-os ~/D/P/T/django_excel (main)> python manage.py migrate
```

Thereafter, run the project:

```bash
(env) sirneij@pop-os ~/D/P/T/django_excel (main)> python manage.py run
```

## Run tests locally

To run the tests, run the following in your terminal:

```bash
(env) sirneij@pop-os ~/D/P/T/django_excel (main)> py.test --nomigrations --reuse-db -W error::RuntimeWarning --cov=core --cov-report=html tests/
```

[1]: https://dev.to/sirneij/django-and-openpyxl-extracting-and-sending-django-model-data-as-excel-file-xlsx-ll3 'Django and Openpyxl: Extracting and Sending Django model data as excel file (.xlsx)'
[2]: https://django-excel-export.herokuapp.com/ 'Live app version'
