import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

DATABASE_NAME = "capstone_test"
DATABASE_PATH = "postgresql://{}/{}".format('localhost:5432', DATABASE_NAME)

# Actor Tests
class ActorTestCase(unittest.TestCase):
    """This class represents the actor test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "capstone_test"
        self.database_path = DATABASE_PATH
        setup_db(self.app, self.database_path)

        # actor for successful add
        self.new_actor ={
            'name': 'Ted Mackrel', 
            'age': '74', 
            'gender': 'Unknown'
        }

        #question for unsucessful add
        self.bad_actor ={
            'name': 'Ted Mackrel', 
            'age': None, 
            'gender': 'Unknown'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET /actors good
    def test_get_actors_good(self):
        """Test that get actors returns 200"""
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # GET /actors bad

    # DELETE /actors good

    # DELETE /actors bad

    # POST /actors good

    # POST /actors bad

    # PATCH /actors good

    # PATCH /actors bad


# Movie Tests
class MovieTestCase(unittest.TestCase):
    """This class represents the movie test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "capstone_test"
        self.database_path = DATABASE_PATH
        setup_db(self.app, self.database_path)

        # actor for successful add
        self.new_movie ={
            'title': 'Working test movie', 
            'releaseDate': 'Thu, 20 Jan 2011 00:00:00 GMT'
        }

        #question for unsucessful add
        self.bad_movie ={
            'title': 'Bad test movie', 
            'releaseDate': 'sdfdsfd'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET /movies good
    def test_get_movies_good(self):
        """Test that gets movies returns 200"""
        res = self.client().get('/movies')
        data = json.loads(res.data)
        print('Movies:',data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # GET /movies bad

    # DELETE /movies good

    # DELETE /movies bad

    # POST /movies good

    # POST /movies bad

    # PATCH /movies good

    # PATCH /movies bad


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()