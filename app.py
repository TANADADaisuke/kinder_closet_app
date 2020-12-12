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
    @requires_auth('get:clothes')
    def retrieve_clothes(payload):
        """Get clothes from our database server.

        Returns: json object with following attributes
        {
            'success': True,
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
    @requires_auth('post:clothes')
    def create_person(payload):
        """Post a new clothes to our database server.

        Returns: json object with following attributes
        {
            'success': True,
            'clothes': formatted clothes which has been just created
        }
        """
        # set error status
        error = False
        # get posted data from json request
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
    
    @app.route('/clothes/<int:clothes_id>', methods=['PATCH'])
    @requires_auth('patch:clothes')
    def update_clothes_data(payload, clothes_id):
        """Update clothes data of given id.

        Returns: json object with following attributes
        {
            'success': True,
            'clothes': formatted clothes which has been just updated
        }
        """
        clothes = Clothes.query.get(clothes_id)
        # exception for not existing id
        if clothes is None:
            abort(404)
        # set error status
        error = False
        # get posted data from json request
        body = request.get_json()
        # update clothes data
        keys = body.keys()
        try:
            if 'type' in keys:
                clothes.type = body['type']
            if 'size'in keys:
                clothes.size = body['size']
            clothes.update()
            formatted_clothes = clothes.format()
        except Exception:
            clothes.rollback()
            error = True
            print(sys.exc_info())
        finally:
            clothes.close_session()
        
        if error:
            abort(400)

        return jsonify({
            'success': True,
            'clothes': formatted_clothes
        })


    @app.route('/clothes/<int:clothes_id>', methods=['DELETE'])
    @requires_auth('delete:clothes')
    def delete_clothes(payload, clothes_id):
        """Delete the given clothes.

        Returns: json object with following attribute
        {
            'success': True,
            'deleted': id of deleted clothes
        }
        """
        clothes = Clothes.query.get(clothes_id)
        # exception for not existing id
        if clothes is None:
            abort(404)
        # set error status
        error = False
        # delete the given clothes
        try:
            clothes.delete()
        except Exception:
            clothes.rollback()
            error = True
            print(sys.exc_info())
        finally:
            clothes.close_session()
        
        if error:
            abort(400)
        
        return jsonify({
            'success': True,
            'deleted': clothes_id
        })

    # Users
    # ----------------------------------------
    @app.route('/users')
    @requires_auth('get:users')
    def retrieve_users(payload):
        """Get users from our database server.
        
        Returns: json object with following attributes
        {
            'success': True,
            'total': num of users stored in our server.
            'users': array of each formatted users
        }
        """
        selection = User.query.all()
        users = []
        for item in selection:
            formatted_user = item.format()
            users.append(formatted_user)
        
        return jsonify({
            'success': True,
            'total': len(users),
            'users': users
        })

    @app.route('/users', methods=['POST'])
    @requires_auth('post:users')
    def create_user(payload):
        """Create a new user.
        
        Returns: json object with following attributes
        {
            'success': True,
            'user': formatted user which has been just created
        }
        """
        # set error status
        error = False
        # get posted data from json request
        body = request.get_json()
        keys = body.keys()
        # if request does not have json body, abort 400
        if body is None:
            abort(400)
        # if json does not have key 'e_mail', abort 400
        if 'e_mail' not in keys:
            abort(400)
        # create a new user
        e_mail = body['e_mail']
        if 'addess' in keys:
            address = body['address']
        else:
            address = ''
        try:
            user = User(
                e_mail=e_mail,
                address=address
            )
            user.insert()
            formatted_user = user.format()
        except Exception:
            user.rollback()
            error = True
            print(sys.exc_info())
        finally:
            user.close_session()
        
        if error:
            abort(400)
        else:
            return jsonify({
                'success': True,
                'user': formatted_user
            })

    @app.route('/users/<int:user_id>', methods=['PATCH'])
    @requires_auth('patch:users')
    def update_user_data(payload, user_id):
        """Update user date of given id.

        Returns: json object with following attributes
        {
            'success': Ture,
            'user': formatted user which has been just updated
        }
        """
        user = User.query.get(user_id)
        # exception for non existing id
        if user is None:
            abort(404)
        # set error status
        error = False
        # get posted data from json request
        body = request.get_json()
        # update user data
        keys = body.keys()
        try:
            if 'e_mail' in keys:
                user.e_mail = body['e_mail']
            if 'address' in keys:
                user.address = body['address']
            user.update()
            formatted_user = user.formate()
        except Exception:
            user.rollback()
            error = True
            print(sys.exc_info())
        finally:
            user.close_session()
        
        if error:
            abort(400)

        return jsonify({
            'success': True,
            'user': formatted_user
        })

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @requires_auth('delete:users')
    def delete_user(payload, user_id):
        """Delete the given user.

        Returns: json object with following attributes
        {
            'success': True,
            'deleted': id of deleted user
        }
        """
        user = User.query.get(user_id)
        # exception for non existing id
        if user is None:
            abort(404)
        # set error status
        error = False
        # delete the user
        try:
            user.delete()
        except Exception:
            user.rollback()
            error = True
            print(sys.exc_info())
        finally:
            user.close_session()
        
        if error:
            abort(400)
        
        return jsonify({
            'success': True,
            'deleted': user_id
        })

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
