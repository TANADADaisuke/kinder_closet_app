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

        # set test clothes id for patch and delete method test
        self.clothes_id = os.environ['TEST_CLOTHES_ID']
    
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

    # Test for staff access
    # ------------------------------------------------


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



# Make the tests conveniently excecutabe
if __name__ == "__main__":
    unittest.main()
