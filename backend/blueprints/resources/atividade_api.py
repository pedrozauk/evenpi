from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required
from backend.models import Evento, User , Atividades, Certificado, TypeUser
from backend.ext.base import db
from backend.serializing import AtividadesSchema
from flask_marshmallow import exceptions

bp_atividade = Blueprint("atividade", __name__, url_prefix="/api/v1/atividade")

@bp_atividade.route("/get_all", methods=["GET"])
@jwt_required()
def get_all():
    query = Atividades.query.all()
    ativadade_schema = AtividadesSchema(many=True)
    return jsonify(ativadade_schema.jsonify(query))

@bp_atividade.route("/create", methods=["POST"])
@jwt_required()
def create_atividade():
    atividade_schema = AtividadesSchema()
    try:
        nova_atividade = atividade_schema.load(request.json, session=db.session)
    except exceptions.ValidationError as e:
        return jsonify({"error":"Erro ao criar atividade", "message":"Campos obrigatórios em branco"}), 400
    nova_atividade.status = True
    db.session.add(nova_atividade)
    db.session.commit()
    return jsonify({"msg": "sucess",
                   "dados" : atividade_schema.dump(nova_atividade)  
                   })