from flask import Blueprint
from flask import jsonify
from flask import request, send_file, make_response
from backend.utils.pdf import gerar_certificado
from backend.models import Participante, Certificado, ParticipanteAtividade, User, Atividades, Evento
from backend.ext.base import db
from datetime import datetime

bp_certificado = Blueprint("certificado", __name__, url_prefix="/api/v1/certificado")

def carrega_dados_para_certificado(participante_id, atividade_id):
    dados_participante = db.session.query(User).join(Participante).filter(Participante.id == participante_id, Participante.user_id == User.id).first()
    dados_atividade = db.session.query(Atividades).filter(Atividades.id == atividade_id).first()
    dados_evento = db.session.query(Evento).join(Atividades).filter(Atividades.id == atividade_id, Atividades.evento_id == Evento.id).first()
    dados = {
                "nome": dados_participante.name,
                "cpf":dados_participante.cpf,
                "descricao": dados_atividade.descricao,
                "carga_horaria": dados_atividade.carga_horaria,
                "descricao_evento": dados_evento.descricao
    }   

    return dados
    


    

@bp_certificado.route("/", methods=["GET"])
def download_certificado():
    if request.method == "GET":
        
        id_participante = request.args.get("participante_id", None)
        id_atividade = request.args.get("atividade_id", None)
        
        if id_atividade is None or id_atividade is None:
            return jsonify({"msg":"Dados incompletos"})
        participante_atividade = db.session.query(ParticipanteAtividade).filter(ParticipanteAtividade.id_atividade == id_atividade, ParticipanteAtividade.id_participante == id_participante).first()
        atividade = db.session.query(Atividades).filter(Atividades.id == id_atividade).first()
        

        if participante_atividade is None:
            return jsonify(msg="Participante ou Atividade não encontrada")
        
        if participante_atividade.checkin == True and atividade.status == 'F':     
            dados = carrega_dados_para_certificado(id_atividade,id_atividade)
            file = gerar_certificado(dados)
            #cria resposta
            response = make_response(file.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=certificado.pdf'
            response.headers['Content-Type'] = 'application/pdf'
        else:
            return jsonify(msg="Não habilitado para download do certificado")

    return response
