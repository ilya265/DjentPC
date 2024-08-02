
HOW TO START

before install project create mariadb database.
You can find create file nearby as create_db

///////////////////////////////
python -m venv venv;
source venv/bin/activate;
pip install flask;
pip install pymysql;
pip install gunicorn;
gunicorn --bind 127.0.0.1:5000 wsgi:app -w 2
//////////////////////////////


DESCRIPTION:


first of all open linux terminal and write this command. That command create virtual environment

python -m venv venv

then you need to activate virtual environment and install libraries.

source venv/bin/activate
pip install flask
pip install pymysql

You can change DB configs directly in the main.py file

after installing, for launching use this command under virualenv:

gunicorn --bind 127.0.0.1:5000 wsgi:app -w 2

project is available on url: 127.0.0.1:5000

admin panel on url: 127.0.0.1:5000/admin.
login: admin
password: 123

