import json
import unittest
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db

DATABASE_URL = os.environ['TEST_DATABASE_URL']

class ClosetAppTestCase(unittest.TestCase):
    """This class represents the closet app test case"""

    def setUp(self):
        """Difine test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = DATABASE_URL
        setup_db(self.app, self.database_path)

        # bind the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        # set up jwts
        self.user_headers = {
            'Authorization': 'Bearer {}'.format(os.environ['USER_JWT'])
        }
        self.staff_headers = {
            'Authorization': 'Bearer {}'.format(os.environ['STAFF_JWT'])
        }
        self.manager_headers = {
            'Authorization': 'Bearer {}'.format(os.environ['MANAGER_JWT'])
        }

        # set test ids for patch and delete method test
        self.clothes_id = os.environ['TEST_CLOTHES_ID']
        self.user_id = os.environ['TEST_USER_ID']
    
    def tearDown(self):
        """Excecuted after reach test"""
        pass

    # Test for public access
    # ------------------------------------------------
    def test_public_1_access_to_home(self):
        """GET /
        Access will succeed without any token.
        """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_public_2_forbidden_create_clothes(self):
        """POST /clothes
        Public access is forbidden for creating new clothes.
        """
        clothes_type = 'shirt'
        size = '100'
        res = self.client().post(
            '/clothes',
            json={
                'type': clothes_type,
                'size': size
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_public_3_forbidden_retrieve_clothes(self):
        """GET /clothes
        Public access is forbidden for retrieving all clothes.
        """
        res = self.client().get('/clothes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')
    
    def test_public_4_forbidden_update_clothes(self):
        """PATCH /clothes/<id>
        Public access is forbidden for updating given clothes.
        """
        size = '120'
        res = self.client().patch(
            '/clothes/1',
            json={
                'size': size
            })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_public_5_forbidden_delete_clothes(self):
        """DELETE /clothes/<id>
        Public access is forbidden for deleting given clothes.
        """
        res = self.client().delete('/clothes/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    # Test for user access
    # ------------------------------------------------
    def test_user_1_forbidden_create_clothes(self):
        """POST /clothes
        Creating new clothes with user JWT is forbidden.
        """
        clothes_type = 'shirt'
        size = '100'
        res = self.client().post(
            '/clothes',
            json={
                'type': clothes_type,
                'size': size
            },
            headers=self.user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_user_2_retrieve_clothes(self):
        """GET /clothes
        Test retrieving all clothes with user JWT.
        """
        res = self.client().get(
            '/clothes',
            headers=self.user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['clothes'], list), True)
    
    def test_user_3_forbidden_update_clothes(self):
        """PATCH /clothes/<id>
        Updating given clothes with user JWT is forbidden.
        """
        size = '120'
        res = self.client().patch(
            '/clothes/{}'.format(self.clothes_id),
            json={
                'size': size
            },
            headers=self.user_headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_user_4_forbidden_delete_clothes(self):
        """DELETE /clothes/<id>
        Deleting given clothes with user JWT is forbidden.
        """
        res = self.client().delete(
            '/clothes/{}'.format(self.clothes_id),
            headers=self.user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')


    # Test for staff access
    # ------------------------------------------------
    def test_staff_1_create_clothes(self):
        """POST /clothes
        Test creating new clothes with staff JWT.
        """
        clothes_type = 'shirt'
        size = '100'
        res = self.client().post(
            '/clothes',
            json={
                'type': clothes_type,
                'size': size
            },
            headers=self.staff_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['clothes']['type'], clothes_type)
        self.assertEqual(data['clothes']['size'], float(size))

        # set clothes id for sequencing tests
        os.environ['TEST_CLOTHES_ID'] = str(data['clothes']['id'])

    def test_staff_2_retrieve_clothes(self):
        """GET /clothes
        Test retrieving all clothes with staff JWT.
        """
        res = self.client().get(
            '/clothes',
            headers=self.staff_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['clothes'], list), True)
    
    def test_staff_3_update_clothes(self):
        """PATCH /clothes/<id>
        Test updating given clothes with staff JWT.
        """
        size = '120'
        res = self.client().patch(
            '/clothes/{}'.format(self.clothes_id),
            json={
                'size': size
            },
            headers=self.staff_headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['clothes']['size'], float(size))

    def test_staff_4_delete_clothes(self):
        """DELETE /clothes/<id>
        Test deleting given clothes with staff JWT.
        """
        res = self.client().delete(
            '/clothes/{}'.format(self.clothes_id),
            headers=self.staff_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], int(self.clothes_id))

    # Test for manager access
    # ------------------------------------------------
    # ------------------------------
    # access to clothes endpoints
    # ------------------------------
    def test_manager_1_create_clothes(self):
        """POST /clothes
        Test creating new clothes with manager JWT.
        """
        clothes_type = 'shirt'
        size = '100'
        res = self.client().post(
            '/clothes',
            json={
                'type': clothes_type,
                'size': size
            },
            headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['clothes']['type'], clothes_type)
        self.assertEqual(data['clothes']['size'], float(size))

        # set clothes id for sequencing tests
        os.environ['TEST_CLOTHES_ID'] = str(data['clothes']['id'])

    def test_manager_2_retrieve_clothes(self):
        """GET /clothes
        Test retrieving all clothes with manager JWT.
        """
        res = self.client().get(
            '/clothes',
            headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['clothes'], list), True)
    
    def test_manager_3_update_clothes(self):
        """PATCH /clothes/<id>
        Test updating given clothes with manager JWT.
        """
        size = '120'
        res = self.client().patch(
            '/clothes/{}'.format(self.clothes_id),
            json={
                'size': size
            },
            headers=self.manager_headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['clothes']['size'], float(size))

    def test_manager_4_delete_clothes(self):
        """DELETE /clothes/<id>
        Test deleting given clothes with manager JWT.
        """
        res = self.client().delete(
            '/clothes/{}'.format(self.clothes_id),
            headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], int(self.clothes_id))

    # ------------------------------
    # access to users endpoints
    # ------------------------------
    def test_manager_1_create_users(self):
        """POST /users
        Test creating new users with manager JWT.
        """
        e_mail = 'test1@kinder-reuse-closet.com'
        address = 'Minato-ku, Tokyo'
        res = self.client().post(
            '/users',
            json={
                'e_mail': e_mail,
                'address': address
            },
            headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user']['e_mail'], e_mail)
        self.assertEqual(data['user']['address'], address)

        # set users id for sequencing tests
        os.environ['TEST_USER_ID'] = str(data['user']['id'])

    def test_manager_2_retrieve_users(self):
        """GET /users
        Test retrieving all users with manager JWT.
        """
        res = self.client().get(
            '/users',
            headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['users'], list), True)
    
    def test_manager_3_update_users(self):
        """PATCH /users/<id>
        Test updating given user with manager JWT.
        """
        address = 'Takanawa, Minato-ku, Tokyo'
        res = self.client().patch(
            '/users/{}'.format(self.user_id),
            json={
                'address': address
            },
            headers=self.manager_headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user']['address'], address)

    def test_manager_4_delete_users(self):
        """DELETE /users/<id>
        Test deleting given user with manager JWT.
        """
        res = self.client().delete(
            '/users/{}'.format(self.user_id),
            headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], int(self.user_id))


# Make the tests conveniently excecutabe
if __name__ == "__main__":
    unittest.main()
