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
    return sqlite3.connect(app.config['DATABASE'], timeout=5)


# open db connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


# close db connection
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route("/")
def view_activity():

    entries = get_entries_view()
    observers = get_observers()
    activities = get_activities()

    return render_template('activity.html', entries=entries, observers=observers, activities=activities)


def get_observers():
    db = get_db()
    users = db.execute("select id, username from users")
    users_dict = [dict(observerid=row[0], observername=row[1]) for row in users.fetchall()]
    return users_dict


def get_entries_view():
    db = get_db()
    logged_entries = db.execute("select * from activity_view order by date desc, time")
    entries = [dict(observer=row[0], activity=row[1], notes=row[2], date=row[3], time=row[4], length=row[5]) for row
               in logged_entries.fetchall()]
    return entries


def get_activities():
    db = get_db()
    acts = db.execute("select id, activitytype from activitytype")
    acts_dict = [dict(activityid=row[0], activityname=row[1]) for row in acts.fetchall()]
    return acts_dict


@app.route("/log_activity", methods=['POST'])
def log_activity():
    db = get_db()
    notes = request.form.get('notes', None)
    length = request.form.get('length', None)
    observer = request.form.get('observer', None)
    activity = request.form.get('activity', None)

    if observer == "":
        pass
    elif activity == "":
        pass
    else:
        db.execute("insert into activity (entryDatetime, inputUser, activityType, ActivityDescription, activityLengthSec)"
                " values(strftime('%s', 'now'),?,?,?,?)", [observer, activity, notes, length])
        db.commit()
        flash("Entry Successful")

    return redirect(url_for('view_activity'))


@app.route("/admin")
def admin_page():
    del_entries = get_entries_del()
    list_usr = get_users()
    return render_template('admin.html', del_entries=del_entries, list_usr=list_usr)

def get_entries_del():
    db = get_db()
    logged_entries = db.execute("select id, activitydescription from activity order by entrydatetime desc Limit 5")
    entries = [dict(id=row[0], activitydescription=row[1]) for row
               in logged_entries.fetchall()]
    return entries

def get_users():
    db = get_db()
    all_users = db.execute("select id, username from users order by id")
    users = [dict(id=row[0], username=row[1]) for row
             in all_users.fetchall()]
    return users

@app.route("/add_activity", methods=['POST'])
# add to the activity table
def add_activity():
    db = get_db()
    activityType = request.form.get('activityType', None)
    if activityType == "":
        flash("Please input an activity.")
    else:
        db.execute("insert into activityType (activityType) values(?)", [activityType])
        db.commit()
        flash("Activity added")

    return redirect(url_for('admin_page'))


@app.route("/add_user", methods=['POST'])
# add new user
def add_user():
    db = get_db()
    username = request.form.get('username', None)
    if username == "":
        flash("Please input a username.")
    else:
        db.execute("insert into users (username) values(?)", [username])
        db.commit()
        flash("User added")

    return redirect(url_for('admin_page'))

@app.route("/remove_logged_activity", methods=['POST'])
# remove entry
def delete_acts():
    db = get_db()
    activityid = request.form.get('activityid', None)
    if activityid == "":
        flash("Please input an activity id.")
    else:
        db.execute("delete from activity where id = ?", [activityid])
        db.commit()
        flash("Entry Removed")

    return redirect(url_for('admin_page'))

@app.route("/remove_user", methods=['POST'])
# remove user
def delete_user():
    db = get_db()
    userid = request.form.get('userid', None)
    if userid == "":
        flash("Please input a userid.")
    else:
        db.execute("delete from users where id = ?", [userid])
        db.commit()
        flash("Entry Removed")

    return redirect(url_for('admin_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
