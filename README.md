# django_excel

![main](https://github.com/Sirneij/django_excel/actions/workflows/django.yml/badge.svg?branch=main)
![Issues](https://img.shields.io/github/issues/Sirneij/django_excel)
![Forks](https://img.shields.io/github/forks/Sirneij/django_excel)
![Stars](https://img.shields.io/github/stars/Sirneij/django_excel)
![License](https://img.shields.io/github/license/Sirneij/django_excel)

This repository accompanies [this tutorial][1] on dev.to. It has been deployed to Heroku and can be accessed live via [this link][2].

## NOTE: If you use Coingecko's API, when you use my code, `CGSIRNEIJ`, I get some commissions. That can be a good way to help me.

## Run Locally

To run the project locally:

1.  Create a virtual environment using `venv`, `poetry`, `virtualenv`, or `pipenv`. I recommend `virtualenv`.
2.  Activate the virtual environment.
3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Migrate the database:

    ```bash
    python manage.py migrate
    ```

5.  Run the project:

    ```bash
    python manage.py runserver
    ```

6.  In another terminal, issue this command to start celery:
    ```bash
    celery -A django_excel worker -l info -B
    ```

## Run Tests Locally

To run the tests:

```bash
pytest --nomigrations --reuse-db -W error::RuntimeWarning --cov=core --cov-report=html tests/
```

[1]: https://dev.to/sirneij/django-and-openpyxl-extracting-and-sending-django-model-data-as-excel-file-xlsx-ll3 "Django and Openpyxl: Extracting and Sending Django model data as excel file (.xlsx)"
[2]: https://django-excel-export.herokuapp.com/ "Live app version"
