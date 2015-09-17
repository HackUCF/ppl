#!/usr/bin/env python3
import string
from random import SystemRandom

from flask import Flask
from flask import render_template, jsonify
from flask_wtf import Form
from marshmallow import Schema, fields
from werkzeug.exceptions import BadRequest
from wtforms import StringField, validators

from models import Member

app = Flask(__name__)
app.secret_key = ''.join(
    SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in
    range(64))


class SearchForm(Form):
    knights_email = StringField(validators=[validators.DataRequired()])


class MemberSchema(Schema):
    timestamp = fields.DateTime(format='%c')
    name = fields.String()
    knights_email = fields.Email()
    shirt_size = fields.String()
    shirt_gender = fields.String()
    paid_dues = fields.Boolean()


members_schema = MemberSchema(many=True)


@app.route('/', methods=('GET', 'HEAD'))
def index():
    return render_template('index.html', form=SearchForm())


@app.route('/search', endpoint='search', methods=('POST',))
def search():
    form = SearchForm()
    if not form.validate():
        raise BadRequest(description='Form validation error')

    if len(form.knights_email.data) < 2:
        raise BadRequest(description='Search string too small')

    members = Member.query.filter(
        Member.knights_email.contains(form.knights_email.data)
    ).order_by(Member.name).limit(20).all()

    return jsonify({
        'results': members_schema.dump(members)
    })


if __name__ == '__main__':
    app.run()
