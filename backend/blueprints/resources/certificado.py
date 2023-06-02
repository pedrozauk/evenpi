from flask import Blueprint
from flask import jsonify
from flask import request, send_file, make_response
from backend.utils.pdf import gerar_certificado
from backend.models import Participante, Certificado
from backend.ext.base import db


bp_certificado = Blueprint("certificado", __name__, url_prefix="/api/v1/certificado")

@bp_certificado.route("/podebaixar",methods=["GET"])
def verifica_disponibilidade():
    id_participante = request.args.get("id_participante", None)
    id_atividade = request.args.get("id_atividade", None)
    if id_atividade is None or id_atividade is None:
        return jsonify({"msg":"Dados incompletos"})
    pass

    

@bp_certificado.route("/", methods=["GET"])
def download_certificado():
    if request.method == "GET":
        #gera_certificado com dados passados
        
        
        file = gerar_certificado("teste")
        #cria resposta
        response = make_response(file.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=certificado.pdf'
        response.headers['Content-Type'] = 'application/pdf'


    return response
