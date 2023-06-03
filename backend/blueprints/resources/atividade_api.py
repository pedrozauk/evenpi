from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required
from backend.models import Evento, User , Atividades, Certificado, TypeUser, Participante, ParticipanteAtividade
from backend.ext.base import db
from backend.serializing import AtividadesSchema, AtividadeSchemaToEdit
from flask_marshmallow import exceptions

bp_atividade = Blueprint("atividade", __name__, url_prefix="/api/v1/atividade")

@bp_atividade.route("/", methods=["GET", "POST"])
@jwt_required()
def atividade():
    if request.method == "GET":
        query = Atividades.query.all()
        ativadade_schema = AtividadesSchema(many=True)
        return ativadade_schema.jsonify(query)
    
    if request.method == "POST":
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

    


@bp_atividade.route("/<int:id_atividade>", methods=["PATCH"])
@jwt_required()
def edita_atividade(id_atividade: str):
    atividade_schema = AtividadeSchemaToEdit()
    query = Atividades.query.filter(Atividades.id == id_atividade)
    novos_dados = atividade_schema.load(request.json)
    if query:
        query.update(novos_dados)
        db.session.commit()
        return jsonify(msg = "atividade atualizada")
    else:
        return jsonify(msg = "atividade não encontrada")
    



@bp_atividade.route("/participantes/<int:id_atividade>", methods=["GET", "POST", "DELETE"])
@jwt_required()
def get_participantes(id_atividade: int): 
    if request.method == "GET":
        query = ParticipanteAtividade.query.filter(ParticipanteAtividade.id_atividade == id_atividade).all()
        retorno = {"data":[]}
        return jsonify(retorno)
    
    if request.method == "POST":
        atividade_id = id_atividade
        participante_id = request.get_json().get("participante_id")
        if atividade_id is None or participante_id is None:
            return jsonify({"msg": "Dados incompletos"}), 404
        atividade = Atividades.query.filter(Atividades.id == atividade_id).first()
        participante = Participante.query.filter(Participante.id == participante_id).first()
        if atividade is None or participante is None:
            return jsonify({"msg": "Participante ou Atividade não encontrado"}), 404
        participante_atividade = ParticipanteAtividade()
        participante_atividade.id_atividade = atividade_id
        participante_atividade.id_participante = participante_id
        participante_atividade.checkin = False
        participante_atividade.status = True
        db.session.add(participante_atividade)
        db.session.commit()
        return jsonify({"msg": "sucess"}), 200
    
    if request.method == "DELETE":
        atividade_id = id_atividade
        participante_id = request.get_json().get("participante_id")
        if atividade_id is None or participante_id is None:
            return jsonify({"msg": "Dados incompletos"}), 404
        
        atividade = Atividades.query.where(Atividades.id == atividade_id)


@bp_atividade.route("/checkin/<int:id_atividade>",methods=["GET"])
def checkin_participante(id_atividade):
    participante_id = request.get_json().get("participante_id",None)
    if participante_id is None or id_atividade is None:
        return jsonify(msg="Dados Incompletos")
    participante_atividade = db.session.query(ParticipanteAtividade).filter(ParticipanteAtividade.id_participante == participante_id, ParticipanteAtividade.id_atividade == id_atividade).first()
    if participante_atividade is None:
        return jsonify(msg="Participante não encontrado para esta atividade")
    participante_atividade.checkin = True
    db.session.commit()   
    return jsonify(msg="Check-in realizado")

