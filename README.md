# Notes

To refresh the data in the database use
```
psql capstone < capstone.psql
```

To create a requirements.txt file and add to it use:
pip freeze > requirements.txt
after every time a requirment is installed

This project will need the following:
    pip install flask_script
    pip install flask_migrate
    pip install psycopg2-binary
    pip install gunicorn

Create a file named Procfile that contains the following:
    web: gunicorn app:app
This instructs Heroku.  Make sure you're main app is named app.py

Create a file named manage.py that contains the following:
```
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
```

Create a file named setup.sh with your environmental variables.
Then point to it by running the following command:
```
source setup.sh
```

Next run the local migrations using the following:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Next login to Heroku with
```
heroku login
```
Then create a new app with (replacing app-name):
```
heroku create app-name
```

I named my app, hiltz-fsnd-capstone
The output will display a url for the app.
In this case it was:
<https://hiltz-fsnd-capstone.herokuapp.com/ >
and
<https://git.heroku.com/hiltz-fsnd-capstone.git>

Using the git url from above, add a remote using:
```
git remote add heroku heroku_git_url
```

If you recive an error it might be because the remote was already added.
Check to see using:
```
git remote -v
```


Next add the postgres addon to your Heroku upp:
```
heroku addons:create heroku-postgresql:hobby-dev --app hiltz-fsnd-capstone
```
heroku-postgresql is the name of the addon. hobby-dev on the other hand specifies the tier of the addon, in this case the free version which has a limit on the amount of data it will store, albeit fairly high.

Double check that it installed with this:
```
heroku config --app hiltz-fsnd-capstone
```
That will also give you the database URL for the heroku instance.

In the browser, go to your Heroku Dashboard (heroku.com) and access your application's settings. Reveal your config variables and start adding all the required environment variables for your project. For the purposes of the sample project, just add one additional one - ‘EXCITED’ and set it to true or false in all lowercase.

Now push it:
```
git push heroku master
```

After it is running, you can run migrations using:
```
heroku run python manage.py db upgrade --app hiltz-fsnd-capstone
```

To test out the app, go to your dashboard an run the app.

# Virtual Enviornment Creation and Use

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

On Windows, run the following:
    py -m pip install --user virtualenv
    py -m venv venv
The last variable above is the name of the virtual environment.  In this case 'venv'
Then add the env folder to the gitignore
Then activate the virtual environment by running:
    .\venv\Scripts\activate
If the above doesn't work, use:
    source venv/Scripts/activate
Check to see if its running, run:
    where python
It should display something allong the lines of (...env\Scripts\python.exe) if it's running.
To leave the virtual environment, run:
    deactivate

## Testing
To run the tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.psql
python test_app.py
```


## Running the server

From within this directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
    - roofuseat.us.auth0.com
3. Create a new, single page web application
    - Name: capstone
    - ClientID: iBZEqTPtTRIsnCwl3YlQSzMZb9zwZ01j
4. Create a new API
    - Name: capstone
    - Identifier: capstone
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `get:movies`
    - `delete:actors`
    - `delete:movies`
    - `post:actors`
    - `post:movies`
    - `patch:actors`
    - `patch:movies`
6. Create new roles for:
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
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the assistant, director, and producer.
         - Not ideal for an actual API, but here are the test users:
            - assistant@test.com 1234asdfQWER
            - director@test.com 1234asdfQWER
            - producer@test.com 1234asdfQWER
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and 
        including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

To get the jwt use
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&
redirect_uri={{YOUR_CALLBACK_URI}}
For this project use: https://roofuseat.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=iBZEqTPtTRIsnCwl3YlQSzMZb9zwZ01j&redirect_uri=https://localhost:8100/
Go to that url, login, and retrive the jwt from the url after login.
Use this in a private browser session to prevent auto sign in

Clock is not an attribute of the time module.  Error in sqlalchemy.  To fix change the following:
in backend\env\Lib\site-packages\sqlalchemy\util\compat.py
replace time_func = time.clock
with time_func = time.perf_counter

Barista: https://localhost:8100/tabs/user-page#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5abkRKUkhQUmhMZnY0US13Y3VyMyJ9.eyJpc3MiOiJodHRwczovL3Jvb2Z1c2VhdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMzhiM2U3Nzk3YzEwMDEzNzAyMTNkIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTkzMTg1NDk3LCJleHAiOjE1OTMyNzE4OTcsImF6cCI6ImRKUmVhSXJ4YlVibTBrRlJsaVZ5ME5Kc2lqbEtWUzBmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.0hp_Ylj_NzHAdp6VlUDiLqvZ_qkdCSV19He53YO5ZLb2kDwu9ajcIhSHEDXXrCxN5Y6-VWr4SREMDYxyttJiny40tx268l25LOIaDzZ0k6QNb4wy2Dv2OUKeQ175aYRsTLosJruL159jw7bMVVcIZFykIMtGCcKfNW0kkYBAcQ_B-yiKiW2Ng_o9NnZv5uDGgveqFG5uA3vaKjZqhGK95dq8edvsiF7rZm_3k2AqtW3mx-o8amjDmJnWFdSz0GaJ2cRorN92zpKiR-L9J7SY1ERuSqVreF89bQmYPrmASO8-5lG9FOPtTAIguEGn6C9tE7zy9k1kL_xK9y3X74-zvg&expires_in=86400&token_type=Bearer

Manager: https://localhost:8100/tabs/user-page#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5abkRKUkhQUmhMZnY0US13Y3VyMyJ9.eyJpc3MiOiJodHRwczovL3Jvb2Z1c2VhdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMzhiNjI3Nzk3YzEwMDEzNzAyMTNmIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTkzMTg1NTMxLCJleHAiOjE1OTMyNzE5MzEsImF6cCI6ImRKUmVhSXJ4YlVibTBrRlJsaVZ5ME5Kc2lqbEtWUzBmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.OMCRTex0PW2eco-iCCLxA2eoNUBFHpFs1v81V7DfxjPTCcIl97yb4qSFegRgMnARrT-QgxB5uajfiFp3XbCKmcG7PWtfDxb9QOwk6SaWpLbddhgFngyAOVIn9J4F0jGW74YDwoG1SPGAD18XkNZ9uvnXk1jCP9hZ6QIj8W9Soq2T82uXc6AUy6_qKAi7_NRWPahWsKtOn8NILU3hebqxwinbjU7GgQZY2w0OR6IYqWhF_sYBHiWhkfSTOnnuQgQYZkiwYS2IOp9LEdkJNRt4CpOPRiaIubt3fEboPzqL3zGXet6U-bmddCzDzX1wBXBkj-L4SksQEsweYC9XI3uDQQ&expires_in=86400&token_type=Bearer