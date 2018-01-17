from flask import Flask, render_template, session, redirect, url_for, flash, abort
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
import json
from flask_wtf import FlaskForm
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

SCORES_PATH = os.path.join(basedir, 'scores/')

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


class LoginForm(FlaskForm):
    name = StringField('学号',validators=[])
    pwd = StringField('姓名',validators=[])
    submit = SubmitField('登陆')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

USERS = {
        '14307090166':  {'name':'何秋月','group':1},
        '15307090012':  {'name':'陈延','group':1},
        '15307090103':  {'name':'刘铁枫','group':1},
        '15307090106':  {'name':'陈家心','group':1},
        '15307090159':  {'name':'费美林','group':1},
        '15307090221':  {'name':'安芯','group':1},
        '15307090036':  {'name':'黄桂彬','group':2},
        '15307090068':  {'name':'沈诗怡','group':2},
        '15307090151':  {'name':'付若男','group':2},
        '15307090192':  {'name':'辛颖','group':2},
        '15307090209':  {'name':'覃丽文','group':2},
        '17349060037':  {'name':'丰雪明','group':2},
        '15307090023':  {'name':'郜宸','group':3},
        '15307090128':  {'name':'祁迪','group':3},
        '15307090188':  {'name':'曹耀之','group':3},
        '15307090210':  {'name':'桑吉卓玛','group':3},
        '15307090218':  {'name':'于皎娇','group':3},
        '17349060035':  {'name':'毛尧飞','group':3},
        '15307090030':  {'name':'张梦龙','group':4},
        '15307090051':  {'name':'李楠','group':4},
        '15307090176':  {'name':'张叶','group':4},
        '15307090178':  {'name':'郭于晴','group':4},
        '15307090206':  {'name':'群宗','group':4},
        '17349060006':  {'name':'刘鹏','group':4},
        '17349060008':  {'name':'张磊','group':4},
        '15307090042':  {'name':'陈云','group':5},
        '15307090087':  {'name':'候晓雯','group':5},
        '15307090119':  {'name':'王一波','group':5},
        '15307090136':  {'name':'黄钊璇','group':5},
        '15307090139':  {'name':'喻佳乐','group':5},
        '15307090146':  {'name':'胥宇扬','group':5},
        '17349060016':  {'name':'郑古兵','group':5},
        '15307080064':  {'name':'王佳君','group':6},
        '15307090014':  {'name':'张宏','group':6},
        '15307090111':  {'name':'蔡芷心','group':6},
        '15307090141':  {'name':'林嘉','group':6},
        '15307090183':  {'name':'周琳','group':6},
        '15307090193':  {'name':'吉昂拉姆','group':6},
        }

SCORES = {}




@app.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():#True if it is a valid POST request
        uid = form.name.data
        name = form.pwd.data
        if uid not in USERS.keys():
            flash('学号错误')
        elif USERS[uid]['name'] != name:
            flash('姓名错误')
        else:
            # Post/Redirect/Get pattern, reason:
            '''when user submits a form and click refresh, the browser would resend the latest request (which is POST),
            the user will receive a weired warning, and the POST request is sent twice which is always not desired.
            Good practice for web applications is to never leave a POST request as a last request sent by the browser.
            The problem brought by this approach is the form data lost when the POST request ends because it is handled
            with a redirect, the application needs to store the name so that the redirected request can have it and use
            it to build the actual response.
            '''
            #url_for() generates URL using the URL map, so any changes made to route names will be automatically available
            return redirect('/home/'+uid) 
    return render_template('login.html', form=form, name=session.get('name'))

@app.route('/home/<uid>', methods=['GET'])
def home(uid):
    if uid not in USERS.keys():
        abort(404)
    name = USERS[uid]['name']
    group = USERS[uid]['group']
    dataList = []
    for sid in USERS.keys():
        if USERS[sid]['group'] == group and sid != uid:
            dataList.append((USERS[sid]['name'], sid))

    resultList = []
    flashInfo = False
    for sname, sid in dataList:
        if uid in SCORES.keys():
            flashInfo = True
            resultList.append((sname,sid,SCORES[uid][sid]))
        else:
            resultList.append((sname,sid,"0"))

    if flashInfo:
        flash('你已经打过分了，分数如下：')
    else:
        flash('你尚未打分')
    return render_template('table.html', dataList=resultList, name=name, group=group)

@app.route('/post/<scores>', methods=['GET'])
def post(scores):
    lst = scores.split(',')
    count = len(lst) / 2
    res = []
    for i in range(int(count)):
        res.append(tuple(lst[2*len(res):2*len(res)+2]))

    whoami = None
    students = [uid for uid, _ in res]
    whichgroup = USERS[students[0]]['group']
    for uid in USERS.keys():
        if USERS[uid]['group'] == whichgroup and uid not in students:
            whoami = uid

    SCORES[whoami] = dict(res)
    
    import datetime
    with open('{0}{1}.log'.format(SCORES_PATH, datetime.datetime.now()), 'w') as fout:
        json.dump(SCORES, fout)

    return redirect('/home/' + whoami)



if __name__ == '__main__':
    manager.run()
