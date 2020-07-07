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