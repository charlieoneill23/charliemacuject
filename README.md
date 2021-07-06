# charliemacuject
This project interacts with the Macuject organisation in two key ways:
1. Pulls the data locally onto the VM using `Psycopg` as a driver for PostgreSQL in Python. This uses the Heroku database which you will need to have access to.
2. Pushes output (such as CSV files, tables, and figures) to the Macuject Google Drive using the Google Drive API.

## Installing and connecting to Heroku Postgres
Heroku Postgres is a managed SQL database service provided directly by Heroku.

### Installing Heroku CLI
Open up a terminal, and install the CLI:
```
curl https://cli-assets.heroku.com/install.sh | sh
```
Check the version installed by entering `heroku --version`.

Because the GCP notebook won't allow you to open a different window to login, you need to login through the terminal.
```
heroku login -i
```
Then enter your login credentials. Check that the `macuject-prod` has the addon `postgresql-asymmetrical-30305` by typing `heroku addons`.

### Heroku Postgres
You can confirm the names and values of your app’s config vars with the `heroku config` command. In particular, we need the `DATABASE_URL` config var. This contains the URL your app uses to access the database.

Then run the following commands to locally replicate the latest production database:
```
heroku pg:backups:capture --app macuject-prod
heroku pg:backups:download --app macuject-prod
```

## How to set up `Psycopg` as driver for PostgreSQL
_What is PostgreSQL?_ PostgreSQL is a powerful, open source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads. In addition to being free and open source, PostgreSQL is highly extensible. For example, you can define your own data types, build out custom functions, even write code from different programming languages without recompiling your database.

_What is Psycopg?_ Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customised thanks to a flexible objects adaptation system.

### Installing and using `Psycopg`
This README will cover several key aspects of using `Psycopg`:
* Connecting to the PostgreSQL database server
* Creating new PostgreSQL tables in Python
* Inserting data into the PostgreSQL table in Python
* Updating data in the PostgreSQL table in Python 
* Transaction – show you how to perform transactions in Python.
* Querying data from the PostgreSQL tables
* Calling a PostgreSQL function in Python
* Calling a PostgreSQL stored procedure in Python
* Handling PostgreSQL BLOB data in Python
* Deleting data from PostgreSQL tables in Python

#### Connecting to the PostgreSQL database server
Install the package:
```{python}
pip install psycopg2
```
Log in to the PostgreSQL database server using any client tool such as pgAdmin or psql. Use the following statement to create a new database named suppliers in the PostgreSQL database server.
```{python}
CREATE DATABASE suppliers;
```

## How to set up the Google Drive API
Go the appropriate project in the Google Developer Console in GCP.

Click on the main menu, and then _APIs and Services_, and click library. Search for the Google Drive API (it should be the first one to come up). Click on it and click __Enable API__.

Under _Library_ in the menu should be an option called _Credentials_. Click on that, and create a credential ID. The steps are fairly straight-forward. Once this is created, download the JSON file by clicking the download button. This will download the JSON file locally. Change the name of the JSON file to _clients_secret.JSON_ and move it to the appropriate directory.

Once you have the JSON file to access Google Drive, we can install a Python library. Open a new Python file/notebook and install `PyDrive`:
```{python}
pip install pydrive
```

Then use the following code to automatically retrieve the OAuth credentials:
```{python}
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)
```

This will take you to a window where you approve the use of the Drive API. Note that you can configure a `settings.yaml` file to save the appropriate credentials. The information for this can be found in the documentation: https://pythonhosted.org/PyDrive/oauth.html#automatic-and-custom-authentication-with-settings-yaml.
