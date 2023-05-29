from flask import Blueprint
from flask import jsonify
from flask import request, send_file

bp_certificado = Blueprint("certificado", __name__, url_prefix="/api/v1/certificado")

def gera_certificado(id:str):
    pass

bp_certificado.route("download/<id>", methods=["GET"])
def download_certificado(id:str):
    file = gera_certificado(id)
    return send_file(file, as_attachment=True)
