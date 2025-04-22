from flask import Blueprint, jsonify
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Hola desde Flask!"})

@main.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])