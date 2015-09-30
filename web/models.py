import csv

from dateutil.tz import tzoffset
from dateutil.parser import parse as parse_datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///member.db'
db = SQLAlchemy(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True))
    name = db.Column(db.String(255))
    knights_email = db.Column(db.String(254), unique=True)
    preferred_email = db.Column(db.String(254), unique=True)
    paid_dues = db.Column(db.Boolean, default=True)
    shirt_size = db.Column(db.String(3))
    shirt_gender = db.Column(db.String(1))
    json = db.Column(db.Text())



def syncdb():
    db.create_all()


def determine_paid_dues(data):
    return data['Payment Method'] != '' and data['Paid Dues'] == 'Y'


def update_membership(local_csv, timezone=tzoffset('EST', -1*5*60*60)):
    # email: Member()
    members = {}
    with open(local_csv, 'r', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        headings = next(reader)
        for row in reader:
            data = dict(zip(headings, row))
            if '' in data: del data['']
            timestamp = parse_datetime(data['Timestamp']).replace(tzinfo=timezone)
            name = '{} {}'.format(data['First Name'].capitalize(),
                                  data['Last Name'].capitalize())
            knights_email = data['UCF Student Email']
            preferred_email = data['Preferred Email Address']
            shirt_size = data['Shirt Size']
            shirt_gender = data['Shirt Gender']
            jdata = json.dumps(data)
            paid_dues = determine_paid_dues(data)

            member = Member(timestamp=timestamp, name=name,
                            knights_email=knights_email,
                            preferred_email=preferred_email,
                            shirt_gender=shirt_gender, shirt_size=shirt_size,
                            paid_dues=paid_dues, json=jdata)
            members[knights_email] = member

    if members:
        Member.query.delete()
        db.session.commit()
        for _, m in members.items():
            db.session.add(m)
        db.session.commit()
        return members.values()
