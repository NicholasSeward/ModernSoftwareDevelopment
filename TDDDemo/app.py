from flask_sqlalchemy import SQLAlchemy
from flask import request,Flask, jsonify

import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True, unique=False)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

from validate_email_address import validate_email

@app.route('/add_user', methods=['GET'])
def add_user():
    name = request.args.get('name')
    email = request.args.get('email')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if email and not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully", "id": new_user.id})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
