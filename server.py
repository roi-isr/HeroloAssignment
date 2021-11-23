"""Spinning up a Flask server that listens to incoming requests on localhost in port 5000"""
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)

import db
import models

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PROPAGATE_EXCEPTIONS'] = True

CORS(app)

jwt = JWTManager(app)


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

    db_session.close()
    return jsonify({"Message": f"Your message to {body['sender']} was sent successfully!"}), 201


@app.route('/get-all-messages/<username>', methods=['GET'])
@jwt_required()
def get_all_messages_by_username(username):
    unread_only = request.args.get('unread') == "true"

    db_session = db.open_db_session(models.DBSession)

    try:
        user_messages = models.User.get_all_messages(db_session=db_session,
                                                     username=str(username).title(),
                                                     unread_only=unread_only)
    except ValueError as err:
        db_session.close()
        return jsonify({"Message": str(err)}), 404

    db_session.close()
    return jsonify(user_messages), 200


@app.route('/read-message/<username>', methods=['GET'])
@jwt_required()
def read_message(username):
    db_session = db.open_db_session(models.DBSession)
    try:
        unread_user_message = models.User.read_message(db_session=db_session,
                                                       username=str(username).title())
    except ValueError as err:
        db_session.close()
        return jsonify({"Message": str(err)}), 404

    db_session.close()
    return jsonify(unread_user_message), 200


@app.route('/delete-message/<username>', methods=['DELETE'])
def delete_message(username):
    db_session = db.open_db_session(models.DBSession)
    try:
        models.User.delete_message(db_session=db_session,
                                   username=str(username).title())
    except ValueError as err:
        db_session.close()
        return jsonify({"Message": str(err)}), 404

    db_session.close()
    return jsonify({"Message": f"Your message was deleted successfully!"}), 200


@app.route('/auth', methods=["POST"])
def authenticate():
    db_session = db.open_db_session(models.DBSession)
    auth_data = request.get_json(force=True)

    valid_user = models.User.verify_user(db_session=db_session, username=auth_data["username"],
                                         password=auth_data["password"])
    if not valid_user:
        db_session.close()
        return jsonify({"Message": str("Unable to authenticate user. Invalid username or password entered.")}), 404

    # Generate access and refresh tokens for the current logged-in user
    access_token = create_access_token(identity=valid_user.id, fresh=True)
    refresh_token = create_refresh_token(identity=valid_user.id)

    db_session.close()
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def token_refresher():
    curr_user_identity = get_jwt_identity()

    if not curr_user_identity:
        return jsonify({"Message": "Invalid refresh token entered."})

    # Generate new access token for the requesting user
    new_access_token = create_access_token(identity=curr_user_identity, fresh=True)

    return jsonify({
        'access_token': new_access_token
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
