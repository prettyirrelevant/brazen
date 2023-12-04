# Welcome to Brazen!

Brazen is a financial services application that enables the disbursement of funds to users. 


*This page contains basic information required to run and test the application locally. 

## Dependencies

- Python programming language: https://python.org/ 
- Poetry - A virtual environment: https://python-poetry.org/ 
- Django - A python framework: [https://www.djangoproject.com/ ](https://www.djangoproject.com/download/)
- Django Rest Framework: https://www.django-rest-framework.org/ 
  
## Setup

1. Fork the project.
1. Clone your version of the project on your local computer.
1. Run `pip install poetry` to install the environment you'd run the project on locally. 
1. Enter `poetry shell` to activate your environment.
1. Run `poetry install` to install the dependencies required. Read this guide for more information: https://python-poetry.org/docs/basic-usage/#installing-dependencies.
1. Create an *.env.dev* file based on the *.env.example* file, input all the necessary credentials. 
1. Run `python manage.py makemigrations`. 
1. Run `python manage.py migrate`.
1. Run `python manage.py runserver` on your terminal or command line interface to run the server in development mode.
1. Go to `http://127.0.0.1:8000/api` to view.
