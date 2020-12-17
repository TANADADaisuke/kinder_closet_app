import os
import sys
from flask import Flask, request, jsonify, abort, render_template
from flask_cors import CORS
from models import setup_db, Clothes, User, Reserve
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
    def create_clothes(payload):
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
            abort(422)
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
            if 'status' in keys:
                clothes.status = body['status']
            clothes.update()
            formatted_clothes = clothes.format()
        except Exception:
            clothes.rollback()
            error = True
            print(sys.exc_info())
        finally:
            clothes.close_session()
        
        if error:
            abort(422)

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
            abort(422)
        
        return jsonify({
            'success': True,
            'deleted': clothes_id
        })

    @app.route('/clothes/<int:clothes_id>/reservations')
    @requires_auth('get:self_reservations')
    def retrieve_clothes_reservations(payload, clothes_id):
        """Retrieve reservation information about that clothes.
        Users can retrieve information only when the reserved user
        is yourself.
        AUthError will be returned if user_id is not match.

        Returns: json object with following attributes
        {
            'success': True,
            'clothes': formatted clothes of the given clothes_id,
            'user': formatted user who has reserved that clothes,
        }
        or, AuthError when accessing clothes other users have reserved.
        """
        selection = Reserve.query.filter_by(clothes_id=clothes_id).all()
        # if the given clothes has not been reserved, abort 404
        if len(selection) == 0:
            abort(404)
        # if two or more user reserved the same clothe, abort umprocessable
        if len(selection) >= 2:
            abort(422)
        # check if access user_id matches reservation user_id
        # query user
        user = User.query.get(selection[0].user_id)
        reservation_user_id = user.auth0_id
        access_user_id = payload['sub']
        
        if access_user_id != reservation_user_id:
            raise AuthError({
                'code': 'Invalid_claims',
                'description': 'Unauthorized access by user'
            }, 401)

        # query clothes
        clothes = Clothes.query.get(selection[0].clothes_id)

        return jsonify({
            'success': 'True',
            'clothes': clothes.format(),
            'user': user.format()
        })

    @app.route('/clothes/<int:clothes_id>/reservations', methods=['POST'])
    @requires_auth('post:reservations')
    def reserve_clothes(payload, clothes_id):
        """Make a reservation.

        Returns: json object with following attributes
        {
            'success': True,
            'clothes': formatted clothes which has been just reserved,
            'user': formatted user who has just reserved that clothes
        }
        """
        error = False
        # get postd data from json request
        body = request.get_json()
        # if request does not have json body, abort 400
        if body is None:
            abort(400)
        # if json does not have key 'auth0_id', abort 400
        if 'auth0_id' not in body.keys():
            abort(400)
        # if auth0_id in body does not match auth0_id in payload, abort 401
        if body['auth0_id'] != payload['sub']:
            abort(401)

        # query user
        user = User.query.filter_by(auth0_id=payload['sub']).all()
        user = user[0]

        # query clothes
        clothes = Clothes.query.get(clothes_id)
        if clothes is None:
            abort(404)
        # if the clothes has already been reserved, abort 422
        if clothes.status == "reserved":
            abort(422)

        # store reservation data in database
        try:
            reservation = Reserve(
                clothes_id=clothes.id,
                user_id=user.id
            )
            reservation.insert()

            clothes.status = "reserved"
            clothes.update()
            formatted_clothes = clothes.format()
            formatted_user = user.format()
        except Exception:
            reservation.rollback()
            clothes.rollback()
            error = True
            print(sys.exc_info())
        finally:
            reservation.close_session()
            clothes.close_session()
        
        if error:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'clothes': formatted_clothes,
                'user': formatted_user
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
        # if json does not have key 'e_mail' or 'auth0_id, abort 400
        if 'e_mail' not in keys or 'auth0_id' not in keys:
            abort(400)
        # create a new user
        e_mail = body['e_mail']
        auth0_id = body['auth0_id']
        if 'address' in keys:
            address = body['address']
        else:
            address = ''
        try:
            user = User(
                e_mail=e_mail,
                address=address,
                auth0_id=auth0_id
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
            abort(422)
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
            if 'auth0_id' in keys:
                user.auth0_id = body['auth0_id']
            user.update()
            formatted_user = user.format()
        except Exception:
            user.rollback()
            error = True
            print(sys.exc_info())
        finally:
            user.close_session()
        
        if error:
            abort(422)

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
            abort(422)
        
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
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405
    
    @app.errorhandler(422)
    def umprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'umprocessable'
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
