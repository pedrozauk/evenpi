from backend.ext.serial import ma
from backend.models import Evento, User , Atividades, Certificado, TypeUser


class EventoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Evento
        include_fk = True

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    cellphone = ma.auto_field()
    type_user = ma.auto_field()

class AtividadesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Atividades
        load_instance = True

    id = ma.auto_field()
    descricao = ma.auto_field(required=True)
    data = ma.auto_field(required=True)
    palestrante = ma.auto_field(required=True)
    carga_horaria = ma.auto_field(required=True)
    status = ma.auto_field()
    evento_id = ma.auto_field(required=True)
    tipo_atividade = ma.auto_field(required=True)

class AtividadeSchemaToEdit(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Atividades
        include_fk = True    

class CertificadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Certificado
        include_fk = True

class TypeUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TypeUser
        include_fk = True
