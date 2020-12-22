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

## Deploy version hosted URL

This application is hosted via Heroku.

- Base URL:
'https://kinder-reuse-closet.herokuapp.com/'

- Authentication: For accessing each endpoint described below, authorization header is required.
'Authrozation: Bearer JWT'

## Endpoint Library

We have the following endpoints.
- Endpoints:
  - GET /clothes and /users
  - GET /clothes/{clothes_id}/reservations and /user/{user_id}/reservations
  - POST /clothes and /users
  - POST /clothes/{clothes_id}/reservations and /users/{user_id}/reservations
  - PATCH /clothes/{clothes_id} and /users/{user_id}
  - DELETE /clothes/{clothes_id} and /users/{user_id}
  - DELETE /clothes/{clothes_id}/reservations and /users/{user_id}/reservations

Details are described below.

### GET /clothes
- General:
  - Get clothes from our database server.
  - Request Arguments: None
  - Role Base Access Control: User, staff, or manager role is required.
  - Returns: json object with following attributes
    {
        'success': True,
        'total': num of clothes stored in our server,
        'clothes': array of each formatted clothes
    }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/clothes -H 'Authorization: Bearer JWT'
  - Response:'''
    {
        "clothes": [
            {
                "id": 6,
                "registerd": "Fri, 18 Dec 2020 09:18:12 GMT",
                "size": 120.0,
                "status": "reserved",
                "type": "shirt"
            },
            {
                "id": 7,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 15.5,
                "status": "reserved",
                "type": "shoes"
            },
            {
                "id": 9,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 13.5,
                "status": "",
                "type": "shoes"
            },
            {
                "id": 11,
                "registerd": "Fri, 18 Dec 2020 09:18:12 GMT",
                "size": 100.0,
                "status": "reserved",
                "type": "shirt"
            },
            {
                "id": 12,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 100.0,
                "status": "",
                "type": "shirt"
            },
            {
                "id": 14,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 100.0,
                "status": "",
                "type": "shirt"
            },
            {
                "id": 15,
                "registerd": "Fri, 11 Dec 2020 12:51:19 GMT",
                "size": 90.0,
                "status": null,
                "type": "shirt"
            },
            {
                "id": 16,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 90.0,
                "status": "",
                "type": "shirt"
            },
            {
                "id": 17,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 90.0,
                "status": "",
                "type": "shirt"
            },
            {
                "id": 18,
                "registerd": "Fri, 11 Dec 2020 12:56:39 GMT",
                "size": 90.0,
                "status": null,
                "type": "shirt"
            },
            {
                "id": 20,
                "registerd": "Thu, 17 Dec 2020 15:34:26 GMT",
                "size": 90.0,
                "status": "",
                "type": "shirt"
            }
        ],
        "success": true,
        "total": 11
    }
  '''

### GET /users
- General:
  - Get users from our database server.
  - Request Arguments: None
  - Role Base Access Control: Staff or manager role is required.
  - Returns: json object with following attributes
    {
        'success': True,
        'total': num of users stored in our server.
        'users': array of each formatted users
    }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/users -H 'Authorization: Bearer JWT''
  - Response:'''
    {
        "success": true,
        "total": 6,
        "users": [
            {
                "address": "",
                "auth0_id": "test_account_1 | test_1",
                "e_mail": "test1@kinder-reuse-closet.com",
                "id": 1,
                "role": "user"
            },
            {
                "address": "Minato-ku, Tokyo",
                "auth0_id": "test_account_2 | test_2",
                "e_mail": "test2@kinder-reuse-closet.com",
                "id": 4,
                "role": "user"
            },
            {
                "address": "Shibuya-ku, Tokyo",
                "auth0_id": "auth0|5fadbe9e64abac00751e7c61",
                "e_mail": "teststaff@kinder-reuse-closet.com",
                "id": 8,
                "role": "staff"
            },
            {
                "address": "Shibuya-ku, Tokyo",
                "auth0_id": "auth0|5f6d247925dd140078ffbefc",
                "e_mail": "testmanager@kinder-reuse-closet.com",
                "id": 9,
                "role": "manager"
            },
            {
                "address": "Machida-city, Tokyo",
                "auth0_id": "auth0|5fdb49c07567970069085ee9",
                "e_mail": "testuser_2@kinder-reuse-closet.com",
                "id": 10,
                "role": "user"
            },
            {
                "address": "Shibuya-ku, Tokyo",
                "auth0_id": "google-oauth2|103606340396848658678",
                "e_mail": "testuser@kinder-reuse-closet.com",
                "id": 11,
                "role": "user"
            }
        ]
    }
  '''

### GET /clothes/{clothes_id}/reservations
- General:
  - Retrieve a reservation of a certain clothes.
  - Request Arguments: None
  - Role Base Access Control: User, staff, or manager role is required.
  - Returns: json object with following attributes
    {
        'success': True,
        'clothes': formatted clothes of the given clothes_id,
        'user': formatted user who has reserved that clothes
    }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/clothes/7/reservations -H 'Authorization: Bearer JWT''
  - Response:'''
    {
        "clothes": {
            "id": 7,
            "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
            "size": 15.5,
            "status": "reserved",
            "type": "shoes"
        },
        "success": true,
        "user": {
            "address": "Shibuya-ku, Tokyo",
            "auth0_id": "google-oauth2|103606340396848658678",
            "e_mail": "testuser@kinder-reuse-closet.com",
            "id": 11,
            "role": "user"
        }
    }
  '''

### GET /users/{user_id}/reservations
- General:
  - Get all reservations of a certain user.
  - Request Arguments: None
  - Role Base Access Control: User, staff, or manager role is required.
  - Returns: json object with following attributes
    {
        'success': True,
        'clothes': list of formatted clothes which the given user has reserved,
        'user': formatted user who has reserved those clothes
    }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/users/11/reservations -H 'Authorization: Bearer JWT''
  - Response:'''
    {
        "clothes": [
            {
                "id": 7,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 15.5,
                "status": "reserved",
                "type": "shoes"
            }
        ],
        "success": true,
        "user": {
            "address": "Shibuya-ku, Tokyo",
            "auth0_id": "google-oauth2|103606340396848658678",
            "e_mail": "testuser@kinder-reuse-closet.com",
            "id": 11,
            "role": "user"
        }
    }
  '''

### POST /clothes
- General:
  - Post a new clothes to our database server.
  - Request Arguments: type, and size
  - Role Base Access Control: Staff, or manager role is required.
  - Returns: json object with following attributes
    {
        'success': True,
        'clothes': formatted clothes which has been just created
    }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/clothes -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer JWT' -d '{"type":"shirt", "size":"120"}''
  - Response:'''
    {
        "clothes": {
            "id": 21,
            "registerd": "Mon, 21 Dec 2020 12:14:37 GMT",
            "size": 120.0,
            "status": "",
            "type": "shirt"
        },
        "success": true
    }
  '''

### POST /users
- General:
  - Create a new user.
  - Request Arguments: e_mail, address, auth0_id, and role
  - Role Base Access Control: Manager role is required.
  - Returns: json object with following attributes
  {
      'success': True,
      'user': formatted user which has been just created
  }
- Samples:
  - Request: curl http://0.0.0.0:8080/users -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer JWT' -d '{"e_mail":"test_user@kinder-reuse-closet.com", "address":"Shibuya-ku, Tokyo","auth0_id":"auth0|testuser", "role":"user"}''
  - Response:'''
    {
        "success": true,
        "user": {
            "address": "Shibuya-ku, Tokyo",
            "auth0_id": "auth0|testuser",
            "e_mail": "test_user@kinder-reuse-closet.com",
            "id": 12,
            "role": "user"
        }
    }
  '''

### POST /clothes/{clothes_id}/reservations
- General:
  - Users can make a reservation.
  - Request Arguments: auth0_id
  - Role Base Access Control: User role is required.
  - Returns: json object with following attribute
  {
      'success': True,
      'clothes': formatted clothes which has been just reserved,
      'user': formatted user who has just reserved that clothes
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/clothes/7/reservations -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer JWT' -d '{"auth0_id":"google-oauth2|103606340396848658678"}''
  - Response:'''
    {
        "clothes": {
            "id": 7,
            "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
            "size": 15.5,
            "status": "reserved",
            "type": "shoes"
        },
        "success": true,
        "user": {
            "address": "Shibuya-ku, Tokyo",
            "auth0_id": "google-oauth2|103606340396848658678",
            "e_mail": "testuser@kinder-reuse-closet.com",
            "id": 11,
            "role": "user"
        }
    }
  '''

### POST /users/{user_id}/reservations
- General:
  - Users can post reservations through their own user_id.
  - Request Arguments: auth0_id and list of reservations
  - Role Base Access Control: User role is required.
  - Returns: json object with following attributes
  {
      "success": True,
      "clothes": list of formatted clothes which has been just reserved,
      "user": formatted user who has just reserved those clothes   
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/users/11/reservations -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer JWT' -d '{"auth0_id":"google-oauth2|103606340396848658678", "reservations":[6, 10, 11]}''
  - Response:'''
    {
        "clothes": [
            {
                "id": 6,
                "registerd": "Fri, 18 Dec 2020 09:18:12 GMT",
                "size": 120.0,
                "status": "reserved",
                "type": "shirt"
            },
            {
                "id": 11,
                "registerd": "Fri, 18 Dec 2020 09:18:12 GMT",
                "size": 100.0,
                "status": "reserved",
                "type": "shirt"
            }
        ],
        "success": true,
        "user": {
            "address": "Shibuya-ku, Tokyo",
            "auth0_id": "google-oauth2|103606340396848658678",
            "e_mail": "testuser@kinder-reuse-closet.com",
            "id": 11,
            "role": "user"
        }
    }
  '''

### PATCH /clothes/{clothes_id}
- General:
  - Updata clothes data.
  - Request Arguments: At least one of the following; type or size
  - Role Base Access Control: Staff, or manager role is required.
  - Returns: json object with following attributes
  {
      'success': True,
      'clothes': formatted clothes which has been just updated
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/clothes/12 -X PATCH -H 'Content-Type: application/json' -H 'Authorization: Bearer JWT' -d '{"size":"120"}''
  - Response:'''
    {
        "clothes": {
            "id": 12,
            "registerd": "Tue, 22 Dec 2020 00:36:42 GMT",
            "size": 120.0,
            "status": "",
            "type": "shirt"
        },
        "success": true
    }
  '''

### PATCH /users/{user_id}
- General:
  - Update user date of given id.
  - Request Arguments: At least one of the following; e_mail, address, auth0_id, or role
  - Role Base Access Control: Manager role is required.
  - Returns: json object with following attributes
  {
      'success': True
      'user': formatted user which has been just updated
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/users/1 -X PATCH -H 'Content-Type: application/json' -H 'Authorization: Bearer JWT' -d '{"address": "Meguro-ku, Tokyo"}''
  - Response:'''
    {
        "success": true,
        "user": {
            "address": "Meguro-ku, Tokyo",
            "auth0_id": "test_account_1 | test_1",
            "e_mail": "test1@kinder-reuse-closet.com",
            "id": 1,
            "role": "user"
        }
    }
  '''

### DELETE /clothes/{clothes_id}
- General:
  - Delete a clothes from our server.
  - Request Arguments: None
  - Role Base Access Control: Staff, or manager role is required.
  - Returns: json object with following attributes
  {
      'success': True,
      'deleted': id of deleted clothes
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/clothes/7 -X DELETE -H 'Authorization: Bearer JWT''
  - Response:'''
    {
        "deleted": 7,
        "success": true
    }
  '''

### DELETE /users/{user_id}
- General:
  - Delete a certain user.
  - Request Arguments: None
  - Role Base Access Control: Manager role is required.
  - Returns: json object with following attributes
  {
      'success': True,
      'deleted': id of deleted user
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/users/1 -X DELETE -H 'Authorization: Bearer JWT''
  - Response:'''
    {
        "deleted": 1,
        "success": true
    }
  '''

### DELETE /clothes/{clothes_id}/reservations
- General:
  - Users can cancel their own reservations.
  - Request Arguments: None
  - Role Base Access Control: User, staff or manager role is required.
  - Returns: json object with following attributes
  {
      'success': True,
      'clothes': formatted clothes of the given clothes_id,
      'user': formatted user who has canceled that reservation
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/clothes/7/reservations -X DELETE -H 'Authorization: Bearer JWT''
  - Response:'''
    {
        "clothes": {
            "id": 7,
            "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
            "size": 15.5,
            "status": "",
            "type": "shoes"
        },
        "success": true,
        "user": {
            "address": "Shibuya-ku, Tokyo",
            "auth0_id": "google-oauth2|103606340396848658678",
            "e_mail": "testuser@kinder-reuse-closet.com",
            "id": 11,
            "role": "user"
        }
    }
  '''

### DELETE /users/{user_id}/reservations
- General:
  - Delete all reservations of a certain user.
  - Request Arguments: None
  - Role Base Access Control: User, staff, or manager role is required.
  - Returns: json object with following attributes
  {
      "success": True,
      "clothes": list of formatted clothes of which reservations 
                 have been just deleted,
      "user": formatted user who has just canceled those reservations
  }
- Samples:
  - Request: 'curl http://0.0.0.0:8080/users/11/reservations -X DELETE -H 'Authorization: Bearer JWT''
  - Response:'''
    {
        "clothes": [
            {
                "id": 6,
                "registerd": "Fri, 18 Dec 2020 09:18:12 GMT",
                "size": 120.0,
                "status": "",
                "type": "shirt"
            },
            {
                "id": 7,
                "registerd": "Fri, 18 Dec 2020 23:18:38 GMT",
                "size": 15.5,
                "status": "",
                "type": "shoes"
            },
            {
                "id": 11,
                "registerd": "Fri, 18 Dec 2020 09:18:12 GMT",
                "size": 100.0,
                "status": "",
                "type": "shirt"
            }
        ],
        "success": true,
        "user": {
            "address": "Shibuya-ku, Tokyo",
            "auth0_id": "google-oauth2|103606340396848658678",
            "e_mail": "testuser@kinder-reuse-closet.com",
            "id": 11,
            "role": "user"
        }
    }
  '''

## Testing
To run the tests, first create test database and set it in environment variable.
'''bash
export TEST_DATABASE_URL='YOUR_TEST_DATABASE_URL'
dropdb TEST_DATABASE && createdb TEST_DATABASE
python app_test.py
'''
