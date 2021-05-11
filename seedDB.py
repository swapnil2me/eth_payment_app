import os
from random import randint
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session
from flask_qrcode import QRcode
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Time
from flask_marshmallow import Marshmallow

# SQLite DB
dataLocation = '/mnt/5a576321-1b84-46e6-ba92-46de6b117d92/Dump'
DB_URL = 'sqlite:///'+os.path.join(dataLocation, 'database.db')

app = Flask(__name__)
qrcode = QRcode(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

class LoginTable(db.Model):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    hexId = Column(String)
    privateKey = Column(String)

def db_create():
    db.create_all()
    print('Database Created')

def db_drop():
    db.drop_all()
    print('Database Dropped')

def db_seed():
    dummyUser = LoginTable(id = 0,
                      username = 'dummy',
                      hexId = 'dummyHex',
                      privateKey = 'dummyPK')

def add_user(name, hexId, privateKey):
    user = LoginTable(id = randint(1,1000),
                      username = name,
                      hexId = hexId,
                      privateKey = privateKey)
    db.session.add(user)
    db.session.commit()

db_drop()
db_create()
db_seed()

@app.route('/',methods=["POST", "GET"])
def register_user():
    msg = 'sadas'
    if request.method == "POST":
        username = request.form.get("name")
        hexId = request.form.get("hexId")
        privateKey = request.form.get("privateKey")
        add_user(username,hexId,privateKey)
        msg = 'success'
    return render_template('register.html',msg=msg)

if __name__ == '__main__':
    app.run(port=1729)