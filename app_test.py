import unittest
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

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
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Excecuted after reach test"""
        pass

    # Test for public access
    # ------------------------------------------------
    def test_retrieve_clothes(self):
        """Test retrieving all clothes"""
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently excecutabe
if __name__ == "__main__":
    unittest.main()
