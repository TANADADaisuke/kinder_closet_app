import json
import unittest
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

DATABASE_URL = os.environ['DATABASE_URL']

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
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()
    
    def tearDown(self):
        """Excecuted after reach test"""
        pass

    # Test for public access
    # ------------------------------------------------
    def test_home_access(self):
        """Test retrieving all clothes"""
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_retrieve_clothes(self):
        """Test retrieving all clothes"""
        res = self.client().get('/clothes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['clothes'], list), True)
    
    def test_create_clothes(self):
        """Test creating new clothes"""
        clothes_type = 'shirt'
        size = '100'
        res = self.client().post(
            '/clothes',
            json={
                'type': clothes_type,
                'size': size
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['clothes']['type'], clothes_type)
        self.assertEqual(data['clothes']['size'], float(size))

# Make the tests conveniently excecutabe
if __name__ == "__main__":
    unittest.main()
