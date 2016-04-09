import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

app = Flask(__name__)

# change to env var?
app.config.from_pyfile("./config.py")


def init_db():
    """Initiate a new db. Run first time."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    """Connects to DB"""
    return sqlite3.connect(app.config['DATABASE'])


# open db connection
def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = connect_db()
        return db


# close db connection
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not  None:
        db.close()


@app.route("/")
def hello():
    x = 'hello world'
    return (x)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

