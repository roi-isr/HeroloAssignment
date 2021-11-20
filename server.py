"""Spinning up a Flask server that listens to incoming requests on localhost in port 5000"""

from flask import Flask, jsonify, request
import psycopg2
from models import DBSession

# conn = psycopg2.connect("postgresql://roi-isr:123456@localhost:5432/messaging-system")

import models
from models import Message, User
msg = Message(sender="Roi", receiver="Avi", message="Hello!", subject="new msg...")
db_session = DBSession()
db_session.autoflush = True
db_session.add(msg)
db_session.commit()