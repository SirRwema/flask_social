from flask import (Flask, g, render_template, flash, redirect,url_for)
from flask.ext.login import LoginManager

import forms
import models

DEBUG = True
PORT = 8000
HOST ='127.0.0.1'

app = Flask(__name_)
app.secret_key = 'W8>S;542;R.6O4!$_<L4j.3{-WYSBgvCJs}x";tBo-5zDq|3t,A4+yij>-VW}0G'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
@app.before_request
def before_request():
    """ Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """ Close the database connection"""
    g.db.close()
    return response

@app.route('/register', methods=('GET','POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you are registered","success")
        models.User.create_user(
            username = form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/')
def index():
    return 'Hey'


if __name__ == '__main__':
    models.initialize()
    models.User.create_user(
        name='arnoldtumukunde',
        email='artumukunde@gmail.com',
        password='password',
        admin=True
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)