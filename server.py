"""Spinning up a Flask server that listens to incoming requests on localhost in port 5000"""

from flask import Flask, jsonify, request
from models import DBSession

import models
from models import Message, User
db_session = DBSession()
db_session.autoflush = True

user1 = User.get_or_create(db_session, username="Roi")
user2 = User.get_or_create(db_session, username="David")
msg = Message(sender=user1, receiver=user2, message="Hello!", subject="new msg...")
db_session.add(msg)
db_session.commit()