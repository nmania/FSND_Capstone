import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

DATABASE_PATH = os.environ.get('TEST_DATABASE_URL')
PERMISSION = os.environ.get('EXECUTIVE_PRODUCER')
auth_header = {'Authorization': "Bearer " + PERMISSION}

# Actor Tests


class ActorTestCase(unittest.TestCase):
    """This class represents the actor test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = DATABASE_PATH
        setup_db(self.app, self.database_path)

        # actor for successful add
        self.new_actor = {
            'name': 'Ted Mackrel',
            'age': '74',
            'gender': 'Unknown'
        }

        # question for unsucessful add
        self.bad_actor = {
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
        res = self.client().get('/actors', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # GET /actors bad
    def test_get_actors_bad(self):
        """Test that get actors returns 405 due to a bad call"""
        res = self.client().get('/actors/3', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request not allowed')

    # DELETE /actors good
    def test_delete_actor_good(self):
        """Test to make sure an actor can be deleted"""
        actor_id = 1
        res = self.client().delete('/actors/'+str(actor_id),
                                   headers=auth_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(actor, None)

    # DELETE /actors bad
    def test_delete_actor_bad(self):
        """Test to make sure a non-existing
        actor deletion attempt returns a 404"""
        actor_id = 999999
        res = self.client().delete('/actors/'+str(actor_id),
                                   headers=auth_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # POST /actors good
    def test_post_actor_good(self):
        """Test to make sure an actor can be added"""
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # POST /actors bad
    def test_post_actor_bad(self):
        """Test to make sure a poorly formed actor json will retun a 422"""
        res = self.client().post('/actors', json=self.bad_actor,
                                 headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # PATCH /actors good
    def test_update_actor_good(self):
        """Test to make sure an actor can be updated"""
        actor_id = 2
        res = self.client().patch('/actors/'+str(actor_id), json={'age': 100},
                                  headers=auth_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['id'], actor_id)

    # PATCH /actors bad
    def test_update_actor_bad(self):
        """Test to make sure a non-existing actor post attempt returns a 404"""
        actor_id = 99999
        res = self.client().patch('/actors/'+str(actor_id), json={'age': 100},
                                  headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Movie Tests
class MovieTestCase(unittest.TestCase):
    """This class represents the movie test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = DATABASE_PATH
        setup_db(self.app, self.database_path)

        # movie for successful add
        self.new_movie = {
            'title': 'Working test movie',
            'releaseDate': 'Thu, 20 Jan 2011 00:00:00 GMT'
        }

        # question for unsucessful add
        self.bad_movie = {
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
        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # GET /movies bad
    def test_get_movies_bad(self):
        """Test that get movies returns 405 due to a bad call"""
        res = self.client().get('/movies/3', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request not allowed')

    # DELETE /movies good
    def test_delete_movie_good(self):
        """Test to make sure a movie can be deleted"""
        movie_id = 1
        res = self.client().delete('/movies/'+str(movie_id),
                                   headers=auth_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)
        self.assertEqual(movie, None)

    # DELETE /movies bad
    def test_delete_movie_bad(self):
        """Test to make sure a non-existing
        movie deletion attempt returns a 404"""
        movie_id = 999999
        res = self.client().delete('/movies/'+str(movie_id),
                                   headers=auth_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # POST /movies good
    def test_post_movie_good(self):
        """Test to make sure a movie can be added"""
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # POST /movies bad
    def test_post_movie_bad(self):
        """Test to make sure a poorly formed movie json will retun a 422"""
        res = self.client().post('/movies', json=self.bad_movie,
                                 headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # PATCH /movies good
    def test_update_movie_good(self):
        """Test to make sure a movie can be updated"""
        movie_id = 2
        res = self.client().patch('/movies/'+str(movie_id),
                                  json={'title': 'New Title'},
                                  headers=auth_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['id'], movie_id)

    # PATCH /movies bad
    def test_update_movie_bad(self):
        """Test to make sure a non-existing
        movie post attempt returns a 404"""
        movie_id = 99999
        res = self.client().patch('/movies/'+str(movie_id),
                                  json={'title': 'New Title'},
                                  headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
