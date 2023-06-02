from flask import Blueprint
from flask import jsonify
from flask import request, send_file
from backend.utils.pdf import gerar_certificado

bp_certificado = Blueprint("certificado", __name__, url_prefix="/api/v1/certificado")



bp_certificado.route("/", methods=["GET"])
def download_certificado():
    file = gerar_certificado()
    return send_file(file, as_attachment=True)
