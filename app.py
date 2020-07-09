import os
from functools import wraps
from flask import Flask, jsonify, request, abort
from models import setup_db, Actor, Movie
from flask_cors import CORS
import json
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers 
    @app.after_request #app decorator that adds headers to the response (i.e. after request)
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # For the general IP
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    # Actor routes *******************************************
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            # Get the short drink for each drink
            actors_json = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': actors_json
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload,actor_id):

        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()
        
        if actor is None:
            abort(404)  # abort if id is not found
        else:
            try:
                actor.delete()
                # return actor id that was deleted
                return jsonify({
                    'success': True,
                    'deleted': actor_id
                })
            except Exception:
                abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):

        # get the body and put the needed parts into variables
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        search = body.get('search', None)
        
        try:
            if search: # Return the search results
                selection = Actor.query.order_by(Actor.id).filter(
                    Actor.name.ilike('%{}%'.format(search))).all()
                actors_json = [actor.format() for actor in selection]
                return jsonify({
                    'success': True,
                    'actors': actors_json
                })
            else: #Post a new actor
                if not(new_name and new_age
                        and new_gender):
                    abort(422)
                else:
                    actor = Actor(name=new_name,
                                        age=new_age,
                                        gender=new_gender)
                    actor.insert()
                    return jsonify({
                        'success': True,
                        'created': actor.id
                    })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload,actor_id):
        body = request.get_json()  # get the request json to get the body of the request

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        # if this abort is inside the try/catch then 
        # it will always bubble up to the except abort
        if actor is None:  
            abort(404)  # abort if actor id is not found
        else:
            try:
                # Check what attributes are contained in the body and update accordingly
                if 'name' in body:
                    actor.name = body.get('name')
                if 'age' in body:
                    # body data is a string, so this must be coerced into an int
                    actor.age = int(body.get('age'))
                if 'gender' in body:
                    actor.gender = body.get('gender')

                actor.update()

                # return true to let the client know it succedded
                return jsonify({
                    'success': True,
                    'id': actor.id
                })

            except:
                abort(422)


    # Movie routes *****************************************
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            # Get the descriptions of each movie
            movies_json = [movie.format() for movie in movies]
            return jsonify({
                'success': True,
                'movies': movies_json
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload,movie_id):

        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)  # abort if id is not found
        else:
            try:
                movie.delete()
                # return movie id that was deleted
                return jsonify({
                    'success': True,
                    'deleted': movie_id
                })
            except Exception:
                abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):

        # get the body and put the needed parts into variables
        body = request.get_json()
        new_title = body.get('title', None)
        new_release = body.get('releaseDate', None)
        search = body.get('search', None)

        try:
            if search: # Return the search results
                selection = Movie.query.order_by(Movie.id).filter(
                    Movie.title.ilike('%{}%'.format(search))).all()
                movies_json = [movie.format() for movie in selection]
                return jsonify({
                    'success': True,
                    'movies': movies_json
                })
            else: #Post a new movie
                if not(new_title and new_release):
                    abort(422)
                else:
                    movie = Movie(title=new_title,
                                        releaseDate=new_release)
                    movie.insert()

                    return jsonify({
                        'success': True,
                        'created': movie.id
                    })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(payload,movie_id):

        body = request.get_json()  # get the request json to get the body of the request
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        # if this abort is inside the try/catch then 
        # it will always bubble up to the except abort
        if movie is None:  
            abort(404)  # abort if movie id is not found
        else:
            try:
                # Check what attributes are contained in the body and update accordingly
                if 'title' in body:
                    movie.title = body.get('title')
                if 'releaseDate' in body:
                    movie.releaseDate = body.get('releaseDate')

                movie.update()

                # return true to let the client know it succedded
                return jsonify({
                    'success': True,
                    'id': movie.id
                })

            except:
                abort(422)

    # Error handlers********************************************
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found",
            "sys_error": str(error)
        }), 404

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized",
            "sys_error": str(error)
        }), 401

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable",
            "sys_error": str(error)
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request",
            "sys_error": str(error)
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Request not allowed",
            "sys_error": str(error)
        }), 405


    return app

app = create_app()

if __name__ == '__main__':
    app.run()