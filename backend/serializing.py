from backend.ext.serial import ma
from backend.models import Evento, User , Atividades, Certificado


class EventoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Evento
        include_fk = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

class AtividadesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Atividades
        include_fk = True

class CertificadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Certificado
        include_fk = True
