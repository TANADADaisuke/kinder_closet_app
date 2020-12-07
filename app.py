import os
import sys
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, Person
from auth import requires_auth, AuthError

def create_app(test_config=None):

    app = Flask(__name__)
    db = setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    @requires_auth('get:clothes')
    def be_cool(payload):
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/coolkids', methods=['POST'])
    @requires_auth('post:clothes')
    def create_person(payload):
        # set error status
        error = False
        # get posted data from json
        name = request.get_json()['name']
        catchphrase = request.get_json()['catchphrase']
        # create new person
        try:
            person = Person(
                name=name,
                catchphrase=catchphrase
            )
            db.session.add(person)
            db.session.commit()
        except Exception:
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()
        
        if error:
            abort(400)
        else:
            return jsonify({
                "success": True,
                "name": name,
                "catchphrase": catchphrase
            })
    
    @app.route('/coolkids/<int:person_id>')
    def catchup_phrase(person_id):
        person = Person.query.get(person_id)
        # exception for not existing id
        if person is None:
            abort(404)
        # get attributes
        name = person.name
        phrase = person.catchphrase

        return jsonify({
            "success": True,
            "id": person_id,
            "name": name,
            "catchphrase": phrase
        })


    # Error Handling
    @app.errorhandler(AuthError)
    def auth_error(error):
        status_code = error.status_code
        return jsonify({
            'success': False,
            'error': status_code,
            'message': error.error['code'],
            'description': error.error['description']
        }), status_code
    

    return app

app = create_app()

if __name__ == '__main__':
    app.run()