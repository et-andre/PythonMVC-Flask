from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
import psycopg2
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')
app.debug = True
app.secret_key = "Rg@O<z7Jd$C%j;C,aKD?O`8fwC(1$'E~"

toolBar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:1234@127.0.0.1:5435/app'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db = SQLAlchemy(app)

conn = psycopg2.connect(dbname='app', user='app', password='1234', host='127.0.0.1', port='5435')

from app.controllers import *