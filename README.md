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


Clock is not an attribute of the time module.  Error in sqlalchemy.  To fix change the following:
in backend\env\Lib\site-packages\sqlalchemy\util\compat.py
replace time_func = time.clock
with time_func = time.perf_counter

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

assistant@test.com
Casting Assistant: https://localhost:8100/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5abkRKUkhQUmhMZnY0US13Y3VyMyJ9.eyJpc3MiOiJodHRwczovL3Jvb2Z1c2VhdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwNjE5YjE2NTJlNWEwMDE5Y2U1MGY3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTQzMDc4MTAsImV4cCI6MTU5NDM5NDIxMCwiYXpwIjoiaUJaRXFUUHRUUklzbkN3bDNZbFFTek1aYjl6d1owMWoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.lPRJIP_nKg1Qx1lnXooz3uQyzZp8DQW4SLf5_UqWFItDIZTasFnZDE-rujodBypE57Z1OunCPS17wzT3j6UQEyd-r7_IHQ-3xAI9WxiWhELetbEhF2jalfm8yybYOc0MYYlvIHxRkuapybIeNUpsh1PpM0_VGPX0lmiEvX4k6sP-lkLPVIe1g4u8Dsd22n-z4LZLInFl8dAItQLlnjfGLP8QRFgx7kJm1cD29a05bJaU6Lj8mzLoNojIccoUFgsv7e7CiG4_aOhcc4bDMRw0GHZQkoSDzzvOmVVsYNA-MaN9BXbZxOisiqil2hUDMuTdRq0ok74EKKlgXChBo1g5_A&expires_in=86400&token_type=Bearer

director@test.com
Casting Director: https://localhost:8100/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5abkRKUkhQUmhMZnY0US13Y3VyMyJ9.eyJpc3MiOiJodHRwczovL3Jvb2Z1c2VhdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwNjE5ZDc2NTJlNWEwMDE5Y2U1MGZhIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTQzMDc4NTksImV4cCI6MTU5NDM5NDI1OSwiYXpwIjoiaUJaRXFUUHRUUklzbkN3bDNZbFFTek1aYjl6d1owMWoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.mXS7IRZ7j6RynBvrzUqjTp3iJLPvzi4cWhYgPHsVQp5AXVPNBbSO2K4SJkAkVFSnsrLcc9hq95jpWZrYh5XobCcgQdfYVq6aZkY_fDuNmKQejl2okQEkd0jH3ivfDcNoX8uidwtQLiKKb9KLkJstS68S36Oet_HtyHeIN0Dplfk6bRtdGuHejtwHOq08ELUQO0dCyv1gv4fmlitxE5K9ngagvvg0u2gX1Nnk8pMdX3FUHnaPokUPj3KyHYkN_iT7lw0_oxgv0B_sPcPlUTPG92szVGOVyXWX_C8TXDfaGiDkW35jzJ_F89lOtmsiaycpvI3KnoTnRKXxQpR71GRC9A&expires_in=86400&token_type=Bearer

producer@test.com
Executive Producer:  https://localhost:8100/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5abkRKUkhQUmhMZnY0US13Y3VyMyJ9.eyJpc3MiOiJodHRwczovL3Jvb2Z1c2VhdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwNjE5ZjUyZWIzMDMwMDE5Yzg0OWRkIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTQzMDc5MDcsImV4cCI6MTU5NDM5NDMwNywiYXpwIjoiaUJaRXFUUHRUUklzbkN3bDNZbFFTek1aYjl6d1owMWoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.xmNtPbBpm4YTsOHagwjlA5Yu2Dmut06d7SaWWgibsncG2b9f86N6HjwNCs7PUVS0NYjySy_SXP2MOnmZvETnpNsUGY1cDFCc5xIdnRkv8R6OB7cr3McOhhDM3dLfLSilIO5C9FmEFMZ3tmAAlyRVAQjDnnZVIaGJTVkcB5GpbmOGH7IqkLMNM822I5NhxXWNhs7XH30eLVL9j1O6U7VWc73v3gqtatuNuB1TRvswArlRUX2mOdwxJKwMnJPTOBumwx5JJCfaTzMzwFSSpuJNBRSJLjBB2BdbB5GNLQip-flTCM-Nv6AUp4Be-2ME_HvOWkS2fUQWULo5QAJnZYqg6w&expires_in=86400&token_type=Bearer