from flask import Blueprint, jsonify, request
from flask_login import login_required
from models.user import User
from models.prompt import Prompt
from backend.database import db_session

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api.route('/prompts', methods=['GET'])
@login_required
def get_prompts():
    prompts = Prompt.query.all()
    return jsonify([prompt.to_dict() for prompt in prompts])