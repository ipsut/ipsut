from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_peewee.db import Database
from flask import Flask
from flask.ext.qrcode import QRcode
from peewee import *

import shortuuid


DEBUG = True
BASE_URL = 'http://127.0.0.1:5000'
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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

class Scan(db.Model):
    sheet = ForeignKeyField(Sheet)


    
#Forms
class SheetForm(FlaskForm):
    name = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    event = StringField('event', validators=[DataRequired()])




#Event Routes 
@app.route('/events')
def list_event():
    events = Sheet.select(Sheet.event).distinct()
    return render_template('eventList.html', events=events)

#Scan Routes 
@app.route('/s/<uuid>')
def scan(uuid):
    sheet = Sheet.get(uuid=uuid)
    scan = Scan()
    scan.sheet = sheet
    scan.save()
    return "Thanks for checking in"

#Sheet Routes 


@app.route('/create_sheet', methods=('GET', 'POST'))
def create_sheet():
    form = SheetForm()
    if form.validate_on_submit():
        #return  "ddd"
        sheet = Sheet()
        sheet.name = form.name.data
        sheet.description = form.description.data
        sheet.event = form.event.data
        sheet.uuid = shortuuid.uuid()
        sheet.save()
        return redirect(url_for('view_sheet', uuid=sheet.uuid))
    return render_template('create_sheet.html', form=form)

@app.route('/sheet/<uuid>')
def view_sheet(uuid):
    sheet = Sheet.get(uuid=uuid)
    #sheet = {}
    #sheet['id'] = uuid
    sheet.url = BASE_URL + "/s/" + sheet.uuid
    #sheet['title'] = "Redhook"
    #sheet['description'] = 'Woodenville'
    #sheet['event'] = "SeattleBeer"
    return render_template('view_sheet.html', sheet=sheet) 


 
if __name__ == '__main__':
    Sheet.create_table(fail_silently=True)
    Scan.create_table(fail_silently=True)
    app.run(debug=True)

