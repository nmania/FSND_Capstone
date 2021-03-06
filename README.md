# Full Stack Nanodegree Capstone Project

Welcome to the Full Stack Nanodegree Capstone Project.  This project will demostrate how to create a backend server with a database, create authorizations, test the backend, and deploy the backend to Heroku.  First this will create a Flask server with a Postgres database.  Then routes will be created for the two tables in the database (actor and movie).  Routes will include a GET, POST, PATCH, and DELETE method for each table.  Next 3 different users will be created to simulate users that might use these.  Each user will be given a specific role that will limit what they are able to do in the system.  After that is all completed, tests to check the routes and user privlegdes will be run.  Once all tests pass, the system will then be deployed to Heroku and be useable.  The next step after this project is to create a front end that uses this created backend.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment
On Windows, run the following:
```
py -m pip install --user virtualenv
py -m venv venv
```
The last variable above is the name of the virtual environment.  In this case 'venv'
Then add the venv folder to the gitignore
Then activate the virtual environment by running:
```
.\venv\Scripts\activate
```
If the above doesn't work, use:
```
source venv/Scripts/activate
```
Check to see if its running, run:
```
where python
```
It should display something allong the lines of (...venv\Scripts\python.exe) if it's running.
To leave the virtual environment, run:
```
deactivate
```

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup
With Postgres running, create a database using the capstone.psql file provided by running:
```bash
dropdb capstone
createdb capstone
psql capstone < capstone.psql
```

## Running the server
Ensure you are working using your created virtual environment.
Set the source to setup.sh:
```bash
source setup.sh
```
To run the server, execute:

```bash
export FLASK_APP=app.py
flask run --reload
```

## Unit Testing
*** NOTE jwts provided for these tests only last 24 hours after submission!\
To run the unit tests, run:
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```

## RBAC Role Testing
*** NOTE jwts provided for these tests only last 24 hours after submission!\
The delete tests will only work one time.  If a second run of these tests is made, then then some of the delete tests will fail since what they're trying to delete is no longer there due to the previous run.\
In Postman, import the file below and run the tests while the server is running:
- udacity_Capstone.postman_collection.json

## Heroku
To see the app on Heroku go to: https://hiltz-fsnd-capstone.herokuapp.com/

## Endpoints
```
GET /actors
GET /movies
POST /actors
POST /movies
DELETE /actors/${id}
DELETE /movies/${id}
PATCH /actors/${id}
PATCH /movies/${id}
```

### GET '/actors'
- Fetches all the actors in the database.
- Request Arguments: None
- Returns: JSON object with actor details. 
```
{
    "actors": [
        {
            "age": 67,
            "gender": "Female",
            "id": 5,
            "name": "Sharron McDuffy"
        }
    "success": true
}
```

### GET /movies
- Fetches all the movies in the database.
- Request Arguments: None
- Returns: JSON object with movie details. 
```
{
    "movies": [
        {
            "id": 1,
            "releaseDate": "Fri, 28 Sep 2001 00:00:00 GMT",
            "title": "Chess Till Death"
        }
    ],
    "success": true
}
```

### POST /actors
- Creates a new actor
- New actor json should be formatted as such:
```
{
    "name": "Wally Walter",
    "age": 75,
    "gender": "Male"
}
```
- Returns 422 if not all required fields are present (name, age, gender)
- Otherwise returns the id of the newly created actor as such:
```
{
    "created": 8,
    "success": true
}
```

### POST /movies
- Creates a new movie
- New movie json should be formatted as such:
```
{
    "title": "Hey You Guys: The Movie",
    "releaseDate": "Thu, 20 Jan 2021 00:00:00 GMT"
}
```
- Returns 422 if not all required fields are present (title, releaseDate)
- Otherwise returns the id of the newly created actor as such:
```
{
    "created": 7,
    "success": true
}
```

### DELETE /actors/${id}
- Deletes the actor with the unique id given in the uri 
- Returns response 404 if actor doesn't exist
- Returns response 422 if there was a problem deleting the actor
- Returns a json object with the id of the actor deleted: 
```
{
    "deleted": 5,
    "success": true
}
```

### DELETE /movies/${id}
- Deletes the movie with the unique id given in the uri
- Returns response 404 if movie doesn't exist
- Returns response 422 if there was a problem deleting the movie
- Returns a json object with the id of the movie deleted: 
```
{
    "deleted": 2,
    "success": true
}
```

### PATCH /actors/${id}
- Updates the actor with the unique id given in the uri 
- Update should be formatted as such and can use any valid field from the actor table:
```
{
    "name": "Ted Tedders"
}
```
- Returns response 404 if actor doesn't exist
- Returns response 422 if there was a problem updating the actor
- Returns a json object with the id of the actor updated: 
```
{
    "id": 5,
    "success": true
}
```

### PATCH /movies/${id}
- Updates the movie with the unique id given in the uri 
- Update should be formatted as such and can use any valid field from the movie table:
```
{
    "title": "Fight People 5"
}
```
- Returns response 404 if movie doesn't exist
- Returns response 422 if there was a problem updating the movie
- Returns a json object with the id of the movie updated: 
```
{
    "id": 3,
    "success": true
}
```

### Auth0 Roles
- API permissions:
    - `get:actors`: Can access the route GET '/actors'
    - `get:movies`:  Can access the route GET '/movies'
    - `delete:actors`: Can access the routeDELETE /actors/${id}
    - `delete:movies`: Can access the routeDELETE /movies/${id}
    - `post:actors`: Can access the routePOST /actors
    - `post:movies`: Can access the routePOST /movies
    - `patch:actors`: Can access the routePATCH /actors/${id}
    - `patch:movies`: Can access the routePATCH /movies/${id}
- Roles:
    - Casting Assistant
        - `get:actors`
        - `get:movies`
    - Casting Director
        - All actions of a casting assistant plus
        - `delete:actors`
        - `post:actors`
        - `patch:actors`
        - `patch:movies`
    - Executive Producer
        - All actions of a casting director plus
        - `delete:movies`
        - `post:movies`
