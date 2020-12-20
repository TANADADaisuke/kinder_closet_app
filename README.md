# Kinder Reuser Closet Project

## Inroduction

Kinder Reuse Closet is a reusing platform for kinder wears. It is a volantary project managed by non-profit organization and supporting families with small children for a long time. 
This project used to hold a market on weekend and exhibit the kinder wears to be reused, but now is time for digital shifting. This application supports to see all kinder wears stored and get them.
You have to sign up first to use this platform.

### See kinder wears stored:

You can see all the clothes registerd in the project platform. If you find a clothes you want to get, select "reserve" and go to project office. You can check and get the item or if you do not like it, you can cancel the reservation.

### Give kinder wears for this project:

If you have any kinder wears you want to give through this project, you can go ahead to the project offiece and give them to staffs. The staffs will upload the clothes to the project platform and then all users can see the items you have given.

## Getting Started

### Installing Dependencies

#### Python 3.7 or newer

We use python for operating this API. Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working with a virtual environment. Instructions for setting up a virtual envirnment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencids

Once you have your virtual environment setup and running, install dependencies by running:

'''bash
pip install -r requirements.txt
'''

This will install all of the required packages we selected within the 'requirements.txt' file.

#### Key Dependencies

- [Flask](https://palletsprojects.com/p/flask/) is a light WSGI web application framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

- [Flask_CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extention for handling Cross Origin Resource Sharing (CORS).

## Setup for local running

### Database Setup
For running this API in local, create a new database for this application and set its path to environment variable.

'''bash
export DATABASE_URL='YOUR_DATABASE_PATH'
'''

### Running the server
 From within the project directory, ensure you are working using your created virtual environment.

 To run the server, execute:

 '''bash
python app.py
 '''

- Base URL: This app is hosted at the default,
'http://0.0.0.0:8080/'

- Authentication: For accessing each endpoint described below, authorization header is required.
'Authrozation: Bearer JWT'

## Deployed version hosted URL

This application is hosted via Heroku.

- Base URL:
'https://kinder-reuse-closet.herokuapp.com/'

- Authentication: For accessing each endpoint described below, authorization header is required.
'Authrozation: Bearer JWT'

## Endpoint Library

We have the following endpoints.
- Endpoints:
  - GET /clothes and /users
  - GET /clothes/<id> and /uses/<id>
  - GET /clothes/<id>/reservations and /user/<id>/reservations
  - POST /clothes and /users
  - POST /clothes/<id>/reservations and /users/<id>/reservations
  - PATCH /clothes/<id> and /users/<id>
  - DELETE /clothes/<id> and /users/<id>
  - DELETE /clothes/<id>/reservations and /users/<id>/reservations

Details are described below.

### GET /clothes


## Testing
To run the tests, first create test database and set it in environment variable.
'''bash
export TEST_DATABASE_URL='YOUR_TEST_DATABASE_URL'
dropdb TEST_DATABASE && createdb TEST_DATABASE
python app_test.py
'''
