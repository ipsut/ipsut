from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_peewee.db import Database
from flask import Flask
from flask.ext.qrcode import QRcode
from peewee import *

import shortuuid


DEBUG = True
BASE_URL = 'localhost:5000'
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
    description = TextField()
    event = TextField()
    uuid = TextField()

#Forms
class SheetForm(FlaskForm):
    name = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    event = StringField('event', validators=[DataRequired()])



#Route 
@app.route('/create_sheet', methods=('GET', 'POST'))
def create_sheet():
    form = SheetForm()
    if form.validate_on_submit():

        return redirect(stuff)
    return render_template('create_sheet.html', form=form)

@app.route('/sheet/<uuid>')
def view_sheet(uuid):
    sheet = {}
    sheet['id'] = uuid
    sheet['url'] = BASE_URL + "/s/" + sheet['id']
    sheet['title'] = "Redhook"
    sheet['description'] = 'Woodenville'
    sheet['event'] = "SeattleBeer"
    return render_template('view_sheet.html', sheet=sheet) 


 
if __name__ == '__main__':
    app.run(debug=True)
