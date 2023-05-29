from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.models import Evento, User, Participante, Atividades, Ingressos
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

@bp_evento.route("/addParticipante/", methods=["POST"])
@jwt_required()
def addParticipante():
    user_id = request.get_json().get("user_id")
    evento_id = request.get_json().get("evento_id")
    if user_id is None or evento_id is None:
        return jsonify({"msg": "Dados incompletos"}), 404
    user = User.query.where(User.id == user_id).first()
    evento = Evento.query.where(Evento.id == evento_id).first()
    if user and evento:
        participante = Participante()
        ingresso = Ingressos()
        # cria um ingresso para o participante
        ingresso.descricao = "Ingresso para o evento " + evento.descricao
        ingresso.valor = 10
        ingresso.status = True
        ingresso.evento_id = evento_id
        db.session.add(ingresso)
        db.session.commit()
        db.session.refresh(ingresso)

        # CRIA UM PARTICIPANTE
        participante.user_id = user_id
        participante.evento_id = evento_id
        participante.status = True
        participante.ingressos_id = ingresso.id
        db.session.add(participante)
        db.session.commit()
        return jsonify({
            "msg": "participante adicionado",
            "user_id" : user_id,
            "evento_id" : evento_id
        })

@bp_evento.route("/removeParticipante/", methods=["POST"])
@jwt_required()
def remove_participante():
    pass

@bp_evento.route("/participantes/<id>", methods=["GET"])
@jwt_required()
def get_participantes(id:str):
    query = Participante.query.filter(Participante.evento_id == id)
    retorno = {"data":[]}
    for participante in query:
        retorno["data"].append({
            "id" : participante.id,
            "user_id" : participante.user_id,
            "evento_id" : participante.evento_id,
            "status" : participante.status
        })
    return jsonify(retorno)
