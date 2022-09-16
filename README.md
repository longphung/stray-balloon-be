# Introduction

This is Group 1.1 Swinburne Tech Enquiry Project: Stray Balloon backend repository.
The app is written in Django with MongoDb for database.

# Getting Started

This project comes with [Poetry][1] for package management.
To start, [Poetry][1] is required, installation guide can be found here: https://python-poetry.org/docs/

1. Install project dependencies:
```shell
    poetry install
```

2. Although not necessary, t is recommended that the app is in a virtual environment for independent package
   management:
```shell
    python -m venv .
```

3. Then simply apply the migrations for the first time:
```shell
    python manage.py migrate
```

4. You can now run the development server:
```shell
    python manage.py runserver
```

# Documentation

Once server is run, API documentation can be found at endpoint `/api/schema/doc`. Example: `http://localhost:8000/api/schema/redoc/`

![Documentation UI Example](docs/images/documentation-ui-example.png)

[1]: https://python-poetry.org/
