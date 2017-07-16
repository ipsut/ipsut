from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import render_template, request, redirect, url_for, make_response
from flask_wtf.csrf import CSRFProtect
from faker import Factory
from flask import Flask
from flask.ext.qrcode import QRcode
from peewee import *
import shortuuid
from flask_peewee.db import Database
import random
import datetime


expire_date = datetime.datetime.now()
expire_date = expire_date + datetime.timedelta(days=90)
fake = Factory.create()

DEBUG = True
BASE_URL = 'http://127.0.0.1:5000'
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

HERE_ID = "RCcBqUW51xDkxDFrItrv"
HERE_CODE = "d6CepETtb1wSZDG65ScuHQ"

DATABASE = {
    'name': 'example.db',
    'engine': 'peewee.SqliteDatabase',
}

app = Flask(__name__)
app.config.from_object(__name__)

csrf = CSRFProtect(app)
qrcode = QRcode(app)
db = Database(app)




#Models
class Sheet(db.Model):
    name = TextField()
    description = TextField()
    event = TextField()
    uuid = TextField()
    lat = TextField(null = True)
    lon = TextField(null = True)


class Scan(db.Model):
    sheet = ForeignKeyField(Sheet)
    username = TextField()
    event = TextField()



    
#Forms
class SheetForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    event = StringField('Event', validators=[DataRequired()])
    lat = StringField('Lattitude')
    lon = StringField('Longitude')


class SigninForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


#User Routes



#Leaderboard Route
@app.route('/event_leaderboard/<event>')
def event_leaderboard(event):
        leaders = []
        users = Scan.select(Scan.username).distinct()
        for user in users:
            leader = {}
            leader['username'] = user.username
            leader['count'] = Scan.select().where(Scan.username == user.username, Scan.event==event).count()
            leaders.append(leader)
        leaders = sorted(leaders, key=lambda k: k['count'], reverse=True)

        for leader in leaders:
            print(leader)
        return render_template('eventLeader.html', leaders=leaders, event_name=event) 
        
@app.route('/leaderboard')
def leaderboard():
        leaders = []
        users = Scan.select(Scan.username).distinct()
        for user in users:
            leader = {}
            leader['username'] = user.username
            leader['count'] = Scan.select().where(Scan.username == user.username).count()
            leaders.append(leader)
        leaders = sorted(leaders, key=lambda k: k['count'], reverse=True)
        # return "leaders"
        for leader in leaders:
            print(leader)
        # return ">>>"

@app.route('/')
def home():
    eventList = Sheet.select(Sheet.event).distinct()
    leaders = []
    users = Scan.select(Scan.username).distinct()
    for user in users:
        leader = {}
        leader['username'] = user.username
        leader['count'] = Scan.select().where(Scan.username == user.username).count()
        leaders.append(leader)
    leaders = sorted(leaders, key=lambda k: k['count'], reverse=True)
    return render_template('index.html', eventList=eventList, leaderboard = leaders)

@app.route('/signin', methods=('GET', 'POST'))
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        resp = make_response(redirect(url_for('create_sheet')))
        print(form.name.data)
        resp.set_cookie('username', form.name.data, expires=expire_date)
        return resp
    return render_template('signin.html', form=form)

#Event Routes 
@app.route('/events')
def list_event():
    events = Sheet.select(Sheet.event).distinct()
    return render_template('eventList.html', events=events)

#Event Routes 
@app.route('/event/<name>')
def view_event(name):
    sheets = Sheet.select().where(Sheet.event == name)
    return render_template('event.html', event_name=name, sheets=sheets)

#Scan Routes 
@app.route('/scans')
def list_scans():
    scans = Scan.select()
    return render_template('scanList.html', scans=scans)

@app.route('/s/<uuid>')
def scan(uuid):
    sheet = Sheet.get(uuid=uuid)
    scan = Scan()
    scan.sheet = sheet
    scan.username = request.cookies.get('username')
    scan.event = sheet.event
    scan.save()
    return "Thanks for checking in"

#Sheet Routes 

@app.route('/sheets')
def list_sheets():
    sheets = Sheet.select()
    print(sheets.count())
    return render_template('sheetList.html', sheets=sheets)

@app.route('/user/<username>')
def user_scans(username):
    scans = Scan.select().where(Scan.username == username)
    print(scans.count())
    return render_template('user.html', scans=scans)


@app.route('/create_sheet', methods=('GET', 'POST'))
def create_sheet():
    form = SheetForm()
    username = request.cookies.get('username')
    if form.validate_on_submit():
        #return  "ddd"
        sheet = Sheet()
        sheet.name = form.name.data
        sheet.description = form.description.data
        sheet.event = form.event.data
        sheet.uuid = shortuuid.uuid()
        sheet.lat = form.lat.data
        sheet.lon = form.lon.data
        sheet.save()
        return redirect(url_for('view_sheet', uuid=sheet.uuid))
    return render_template('create_sheet.html', form=form, username=username)

@app.route('/sheet/<uuid>')
def view_sheet(uuid):
    sheet = Sheet.get(uuid=uuid)
    #sheet = {}
    #sheet['id'] = uuid
    sheet.url = BASE_URL + "/s/" + sheet.uuid
    #sheet['title'] = "Redhook"
    #sheet['description'] = 'Woodenville'
    #sheet['event'] = "SeattleBeer"
    req = "https://image.maps.cit.api.here.com/mia/1.6/mapview?app_id="+HERE_ID+"&app_code="+HERE_CODE+"&c="+sheet.lon+","+sheet.lat+"&z=15"
    return render_template('view_sheet.html', sheet=sheet, HERE_CODE=HERE_CODE, HERE_ID=HERE_ID, req=req) 


#Simulator Route
@app.route('/simulate')
def simulate():
    simulate_sheets()
    simulate_scans()
    return "hey"
    

def simulate_sheets():
    # return
    for i in range(25):
        print("making sheet")
        sheet = Sheet()
        sheet.name = fake.company()
        sheet.description = fake.address()
        sheet.event = fake.safe_color_name()
        sheet.uuid = shortuuid.uuid()
        sheet.lat = random.randint(1,100)
        sheet.lon = random.randint(1,100)
        sheet.save()
   
def simulate_scans():
    for i in range(25):
        number = random.randint(1,10)
        username = fake.name()
        print(username)
        sheets = Sheet.select().order_by(fn.Random()).limit(number)
        for sheet in sheets:
            print(" scan")
            scan = Scan()
            scan.sheet = sheet
            scan.username = username
            scan.event = sheet.event
            scan.save()
            


    
        
        
    
 
if __name__ == '__main__':

    Sheet.create_table(fail_silently=True)
    Scan.create_table(fail_silently=True)


    app.run(debug=True)

