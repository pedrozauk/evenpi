from flask import Blueprint
from backend.blueprints.resources.auth_api import bp_auth
from backend.blueprints.resources.user_api import bp_user
from backend.blueprints.resources.evento_api import bp_evento
from backend.blueprints.resources.atividade_api import bp_atividade
from backend.blueprints.resources.certificado import bp_certificado


def init_app(app):
    #registra as blueprints das apis
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_evento)
    app.register_blueprint(bp_atividade)
    app.register_blueprint(bp_certificado)
