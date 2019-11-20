## Getting Started

This is an api made by Django and Django-Rest-Framework.
This api is used as an api backend for E-commerse B2C applications

### Prerequisites

Inorder to run the api server one will need 
python 3.7.2 and pip installed and in the path.
```
python manage.py runserver
```

### Installing
First clone the github repository

```
git clone 
```

Go to the root directory and create a virtual environment

```
virtualenv venv
```

activate the virtual environment

In windows
```
venv/Scripts/activate
```
In Linux
```
./venv/bin/activate
```
Install the requirements in requirements.txt
```
pip install -r requirements.txt
```
Run migration on the database
```
python manage.py migrate
```
Run the server
```
python manage.py runserver
```
End with an example of getting some data out of the system or using it for a little demo

## Running the tests

In order to run the tests(assuming the virtual environment is active)

```
python manage.py test
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used.
* [Django Rest Framework](https://www.django-rest-framework.org/) - The django api library used


## Authors

* **Daniel Waruo** - waruodaniel@gmail.com

## License

This project is licensed under the Apache License 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
