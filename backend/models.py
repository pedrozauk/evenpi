# -*- coding: utf-8 -*-
from api.ext.base import db 


                                      


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(250))
    username = db.Column(db.String(100),unique=True)
    tipo_usuario = db.Column(db.Integer, db.ForeignKey("type_user.id"))
    cellphone = db.Column(db.String(11))
    status = db.Column(db.Boolean)
    
class TypeUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100))
    fk_user = db.relationship("User", backref="type_user", lazy=True)
    status = db.Column(db.Boolean)


    
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    descricao = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    data_inicio = db.Column(db.DateTime)
    duracao = db.Column(db.Integer)
    data_fim = db.Column(db.DateTime)

class Participante(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("evento.id"), unique=True)
    certificado_id = db.Column(db.Integer, db.ForeignKey("certificado.id"), unique=True)
    ingressos_id = db.Column(db.Integer, db.ForeignKey("ingressos.id"), unique=True)
    status = db.Column(db.Boolean)

class Certificado(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    carga_horario =  db.Column(db.String(100))
    atividade_id = db.Column(db.Integer, db.ForeignKey("atividades.id"), unique=True)
    status = db.Column(db.Boolean)

class Ingressos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    valor = db.Column(db.Float)
    evento_id = db.Column(db.Integer, db.ForeignKey("evento.id"), unique=True)
    fk_participante = db.relationship("Participante", backref="ingressos", lazy=True) 
    status = db.Column(db.Boolean)

class Atividades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_evento = db.Column(db.Integer, db.ForeignKey("evento.id"), unique=True)
    descricao = db.Column(db.String(100))
    data = db.Column(db.DateTime)
    palestrante = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    tipo_atividade = db.Column(db.Integer, db.ForeignKey("tipo_atividade.id"))
    fk_atividade = db.relationship("ParticipanteAtividade", backref="atividades", lazy=True)

class TipoAtividade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    status = db.Column(db.Boolean)

class ParticipanteAtividade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_participante = db.Column(db.Integer, db.ForeignKey("participante.id"), unique=True)
    id_atividade = db.Column(db.Integer, db.ForeignKey("atividades.id"), unique=True)
    status = db.Column(db.Boolean)
    fk_certificado_participante_atividade = db.relationship("CertificadoParticipanteAtividade", backref="participante_atividade", lazy=True)

class CertificadoParticipanteAtividade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_certificado = db.Column(db.Integer, db.ForeignKey("certificado.id"), unique=True)
    id_participante_atividade = db.Column(db.Integer, db.ForeignKey("participante_atividade.id"), unique=True)


