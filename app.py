from flask import Flask, render_template, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zkz74c5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) #one user has only one role

    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(64), unique=True, nullable=False, default='Student')
    users = db.relationship('User', backref='role') #one role belongs to many users

    def __repr__(self):
        return '<Role %r>' % self.rolename

class ScoreTable(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    scorer = db.Column(db.Integer, index=True)
    scoree = db.Column(db.Integer, index=True)
    score = db.Column(db.Integer, index=True)
    
    def __repr__(self):
        return '<Score Table>'


class LoginForm(Form):
    name = StringField(validators=[Required()])
    pwd = PasswordField(validators=[Required()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():#True if it is a valid POST request
        session['name'] = form.name.data
        # Post/Redirect/Get pattern, reason:
        '''when user submits a form and click refresh, the browser would resend the latest request (which is POST),
            the user will receive a weired warning, and the POST request is sent twice which is always not desired.
            Good practice for web applications is to never leave a POST request as a last request sent by the browser.
            The problem brought by this approach is the form data lost when the POST request ends because it is handled
            with a redirect, the application needs to store the name so that the redirected request can have it and use
            it to build the actual response.
        '''
        #url_for() generates URL using the URL map, so any changes made to route names will be automatically available
        return redirect(url_for('index')) 
    return render_template('login.html', form=form, name=session.get('name'))

if __name__ == '__main__':
    manager.run()
