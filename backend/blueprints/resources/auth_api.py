from flask import jsonify, request
from flask import Blueprint
from flask_jwt_extended import jwt_required , create_access_token , get_jwt_identity, create_refresh_token
from backend.models import User
from backend.ext.base import db
from flasgger import swag_from




bp_auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@bp_auth.route('/login', methods=["POST"])
@swag_from('swagger/auth/login.yml')
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    query = db.session.query(User).where(User.username == username).first()
    if query is None:
        return jsonify({"msg": "Usuário ou senha inválidos"}), 401
    if username != query.username or password != query.password:
        return jsonify({"msg": "Usuário ou senha inválidos"}), 401
    new_token = create_access_token(identity=username)
    new_refresh_token = create_refresh_token(identity=username)
    return jsonify(acess_token = new_token, refresh_token = new_refresh_token)

#rota para fazer refresh no token
@bp_auth.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
@swag_from('swagger/auth/refresh.yml')
def reset_token():
    old_identify = get_jwt_identity()
    new_token = create_access_token(identity=old_identify)
    
    return jsonify(acess_token = new_token)


