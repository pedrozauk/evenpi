# -*- coding: utf-8 -*-
from backend.ext.base import db 


                                      


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(250))
    cpf = db.Column(db.String(11))
    date_birth = db.Column(db.DateTime)
    username = db.Column(db.String(100),unique=True)
    tipo_usuario = db.Column(db.Integer, db.ForeignKey("type_user.id"))
    cellphone = db.Column(db.String(11))
    status = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"User:{self.name}, CPF:{self.cpf}"

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
    atividades = db.relationship('Atividades', backref='evento', lazy=True)
    organizado = db.Column(db.Integer, db.ForeignKey("user.id"))

class Participante(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    evento_id = db.Column(db.Integer, db.ForeignKey("evento.id"))
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
    evento_id = db.Column(db.Integer, db.ForeignKey("evento.id"))
    fk_participante = db.relationship("Participante", backref="ingressos", lazy=True) 
    status = db.Column(db.Boolean)

class Atividades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    data = db.Column(db.DateTime)
    palestrante = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    carga_horaria = db.Column(db.Integer)
    tipo_atividade = db.Column(db.Integer, db.ForeignKey("tipo_atividade.id"))
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'))

class TipoAtividade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    status = db.Column(db.Boolean)

class ParticipanteAtividade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_participante = db.Column(db.Integer, db.ForeignKey("participante.id"))
    id_atividade = db.Column(db.Integer, db.ForeignKey("atividades.id"))
    checkin = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    fk_certificado_participante_atividade = db.relationship("CertificadoParticipanteAtividade", backref="participante_atividade", lazy=True)

class CertificadoParticipanteAtividade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_certificado = db.Column(db.Integer, db.ForeignKey("certificado.id"), unique=True)
    id_participante_atividade = db.Column(db.Integer, db.ForeignKey("participante_atividade.id"), unique=True)


