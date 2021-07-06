# charliemacuject
This project interacts with the Macuject organisation in two key ways:
1. Pulls the data locally onto the VM using `Psycopg` as a driver for PostgreSQL in Python. This uses the Heroku database which you will need to have access to.
2. Pushes output (such as CSV files, tables, and figures) to the Macuject Google Drive using the Google Drive API.

## Installing and connecting to Heroku Postgres
Heroku Postgres is a managed SQL database service provided directly by Heroku.

### Installing Heroku

### Heroku Postgres
Heroku recommends running Postgres locally to ensure parity between environments. There are several pre-packaged installers for installing PostgreSQL in your local environment. Once Postgres is installed and you can connect, you’ll need to export the `DATABASE_URL` environment variable for your app to connect to it when running locally:
```
$ export DATABASE_URL=postgres://$(whoami)
```
`psql` is the native PostgreSQL interactive terminal and is used to execute queries and issue commands to the connected database. To establish a psql session with your remote database, use `heroku pg:psql`. If you have more than one database, specify the database to connect to (just the colour works as a shorthand) as the first argument to the command (the database located at `DATABASE_URL` is used by default). For example, `heroku pg:psql grey`.

`pg:pull` can be used to pull remote data from a Heroku Postgres database to a database on your local machine. The command looks like this:
```
$ heroku pg:pull HEROKU_POSTGRESQL_MAGENTA mylocaldb --app sushi
```
This command creates a new local database named `mylocaldb` and then pulls data from the database at `DATABASE_URL` from the app `sushi`. 

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
