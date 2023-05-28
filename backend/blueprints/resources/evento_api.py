from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.models import Evento
from backend.ext.base import db
from datetime import datetime
from flask_sqlalchemy import session
from backend.ext.base import db
from backend.serializing import EventoSchema
bp_evento = Blueprint("evento", __name__, url_prefix="/api/v1/evento")

@bp_evento.route("/get_all", methods=["GET"])
@jwt_required()
def get_all():
    query = Evento.query.all()
    retorno = {"data":[]}
    evento_schema = EventoSchema(many=True)
    return evento_schema.jsonify(query)

@bp_evento.route("/create", methods=["POST"])
@jwt_required()
def create_evento():
    evento_schema = EventoSchema()
    descricao = request.get_json().get("descricao")
    data_inicio = request.get_json().get("data_inicio")
    data_fim = request.get_json().get("data_fim")
    duracao = request.get_json().get("duracao")
    status = True
    if descricao is None or data_inicio is None or data_fim is None or duracao is None:
        return jsonify({"msg": "Dados incompletos"}), 404
    novo_evento = Evento()
    novo_evento.descricao = descricao
    novo_evento.data_fim = datetime.strptime(data_fim, "%d/%m/%Y %H:%M:%S")
    novo_evento.data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y %H:%M:%S")
    novo_evento.duracao = duracao
    novo_evento.status = status
    db.session.add(novo_evento)
    db.session.commit()
    db.session.refresh(novo_evento)
  
    return jsonify({"msg": "sucess",
                    "data": evento_schema.dump(novo_evento)})

@bp_evento.route("/edit/<id>", methods=["PATCH"])
@jwt_required()
def editaEvento(id: str):
    evento_schema = EventoSchema()
    query = Evento.query.filter(Evento.id == id)
    novos_dados = evento_schema.load(request.json)
    if query:
        query.update(novos_dados)
        db.session.commit()
        return jsonify(msg = "evento atualizado")
    else:
        return jsonify(msg = "evento não encontrado")


@bp_evento.route("/deactivate/<id>", methods=["GET"])
@jwt_required()
def desativa_evento(id:str):

    evento = Evento.query.where(Evento.id == id).first()
    evento.status = False
    db.session.commit()
    return jsonify({
        "msg": "evento desativado",
        "id" : evento.id,
        "status" : evento.status
    })

@bp_evento.route("/activate/<id>", methods=["GET"])
@jwt_required()
def ativa_evento(id:str):
    evento = Evento.query.where(Evento.id == id).first()
    evento.status = True
    db.session.commit()
    return jsonify({
        "msg": "evento ativado",
        "id" : evento.id,
        "status" : evento.status
    })