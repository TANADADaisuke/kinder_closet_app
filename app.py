import os
import sys
from flask import Flask, request, jsonify, abort, render_template
from flask_cors import CORS
from models import setup_db, Clothes, User
from auth import requires_auth, AuthError

def create_app(test_config=None):

    # App Config
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ---------------------------------------- #
    # Endpoints
    # ---------------------------------------- #
    @app.route('/')
    def index():
        # return render_template('pages/home.html')
        return 'Welcome to Kinder Reuse Closet!'

    # Clothes
    # ----------------------------------------
    @app.route('/clothes')
    # @requires_auth('get:clothes')
    def retrieve_clothes():
        """Get clothes from our database server.

        Returns: json object with following attributes
        {
            'success': Ture,
            'total': num of clothes stored in our server,
            'clothes': array of each formatted clothes
        }
        """
        selection = Clothes.query.all()
        clothes = []
        for item in selection:
            formatted_clothes = item.format()
            clothes.append(formatted_clothes)

        return jsonify({
            'success': True,
            'total': len(clothes),
            'clothes': clothes
        })

    @app.route('/clothes', methods=['POST'])
    # @requires_auth('post:clothes')
    def create_person():
        """Post a new clothes to our database server.

        Returns: json object with following attributes
        {
            'success': True,
            'clothes': formatted clothes which has been just created
        }
        """
        # set error status
        error = False
        # get posted data from json
        body = request.get_json()
        # if request does not have json body, abort 400
        if body is None:
            abort(400)
        # if json does not have key 'type' and 'size', abort 400
        keys = body.keys()
        if 'type' not in keys or 'size' not in keys:
            abort(400)
        # create new clothes
        clothes_type = body['type']
        size = body['size']
        try:
            clothes = Clothes(
                type=clothes_type,
                size=size
            )
            clothes.insert()
            formatted_clothes = clothes.format()
        except Exception:
            clothes.rollback()
            error = True
            print(sys.exc_info())
        finally:
            clothes.close_session()
        
        if error:
            abort(400)
        else:
            return jsonify({
                'success': True,
                'clothes': clothes.format()
            })
    
    @app.route('/clothes/<int:clothes_id>')
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

    # Users
    # ----------------------------------------


    # Error Handling
    # ----------------------------------------
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
    app.run(host='0.0.0.0', port=8080, debug=True)
