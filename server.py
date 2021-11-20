"""Spinning up a Flask server that listens to incoming requests on localhost in port 5000"""

from flask import Flask, jsonify, request
import db
import models
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/write-message', methods=['POST'])
def write_message():
    body = request.get_json(force=True)

    db_session = db.open_db_session(models.DBSession)

    sender = models.User.get_user(db_session=db_session, username=str(body["sender"]).title())
    receiver = models.User.get_user(db_session=db_session, username=str(body["receiver"]).title())
    message = models.Message(
        sender=sender,
        receiver=receiver,
        subject=body["subject"],
        message=body["message"]
    )

    db.write(db_session=db_session, model_instance=message)

    return jsonify({"Message": f"Your message to {body['sender']} was sent successfully!"}), 201


@app.route('/get-all-message/<username>', methods=['GET'])
def get_all_messages_by_username(username):
    db_session = db.open_db_session(models.DBSession)

    try:
        user_messages = models.User.get_all_messages(db_session=db_session, username=str(username).title())
    except ValueError:
        return jsonify({"Message": "The user specified doesn't exist"}), 404

    return jsonify(user_messages), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
