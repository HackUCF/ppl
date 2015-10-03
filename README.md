# ppl
Google Sheets-backed membership lookups with Flask, Skeleton, and Django.

![Screenshot](https://raw.githubusercontent.com/HackUCF/ppl/gh-pages/screenshot.png)

## Installation and Configuration
### Python 3:

1. `$ pip install -r requirements.txt` for dependencies
2. `$ ./manage.py syncdb` to create the SQLite database
3. `$ ./manage.py update --noauth_local_webserver` to authorize the application to update itself

### Python 2:

1. Update to Python 3
2. Follow the [Python 3 instructions](#python-3)