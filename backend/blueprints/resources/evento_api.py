from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.models import Evento
from backend.ext.base import db
from datetime import datetime
from flask_sqlalchemy import session
from backend.ext.base import db
bp_evento = Blueprint("evento", __name__, url_prefix="/api/v1/evento")

@bp_evento.route("/get_all", methods=["GET"])
@jwt_required()
def get_all():
    query = Evento.query.all()
    retorno = {"data":[]}
    for evento in query:
        retorno["data"].append({
                                    "evento":evento.descricao, 
                                    "data_inicio":evento.data_inicio.isoformat(), 
                                    "status": evento.status,
                                    "data_fim":evento.data_fim.isoformat(),
                                    "duracao": evento.duracao,
                                    "id": evento.id
                                    })
        
    return jsonify(retorno)

@bp_evento.route("/create", methods=["POST"])
@jwt_required()
def create_evento():
    descricao = request.get_json().get("descricao")
    data_inicio = request.get_json().get("data_inicio")
    data_fim = request.get_json().get("data_fim")
    duracao = request.get_json().get("duracao")
    status = True
    if descricao is None or data_inicio is None or data_fim is None or duracao is None:
        return jsonify({"msg": "Dados incompletos"})
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
                    "data":{
                                "id": novo_evento.id,
                                "evento": novo_evento.descricao,
                                "data_inicio": novo_evento.data_inicio.isoformat(),
                                "data_fim": novo_evento.data_fim.isoformat(),
                                "duracao": novo_evento.duracao,
                                "status": novo_evento.status
                                }})

@bp_evento.route("/edit/<id>", methods=["PATCH"])
@jwt_required()
def editaEvento(id: str):
    query = Evento.query.where(Evento.id == id).first()
    if query:
        return jsonify(msg = "evento existe")
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