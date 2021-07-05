# charliemacuject
This project interacts with the Macuject organisation in two key ways:
1. Pulls the data locally onto the VM using`Psycopg` as a driver for PostgreSQL in Python.
2. Pushes output (such as CSV files, tables, and figures) to the Macuject Google Drive using the Google Drive API.

## How to set up Psycopg as driver for PostgreSQL
_What is PostgreSQL?_ PostgreSQL is a powerful, open source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads. In addition to being free and open source, PostgreSQL is highly extensible. For example, you can define your own data types, build out custom functions, even write code from different programming languages without recompiling your database.

_What is Psycopg?_ Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customized thanks to a flexible objects adaptation system.

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
