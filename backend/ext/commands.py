import click
from backend.ext.base import db
from backend.models import User, Atividades, Evento
from datetime import datetime

def create_db():
    """ Criar o banco"""
    db.create_all()

def drop_db():
    db.drop_all()


def populate():
    novo_user = User()
    novo_user.cellphone = "66999999999"
    novo_user.cpf = "00000000000"
    novo_user.date_birth = datetime(2000,5,5)
    novo_user.name = "usuario teste"
    novo_user.username = "teste.user"
    novo_user.password = "12345"
    data = [
                novo_user,
                Evento( descricao="evento 1 para teste", 
                        status = True, 
                        data_inicio = datetime(2023,3,2),
                        duracao = 100,
                        data_fim = datetime(2023,3,20)
                        ),
                Evento( descricao="evento 2 para teste", 
                        status = True, 
                        data_inicio = datetime(2023,5,22),
                        duracao = 10,
                        data_fim = datetime(2023,5,25)
                ),
                Evento( descricao="evento 3 para teste", 
                        status = False, 
                        data_inicio = datetime(2023,4,10),
                        duracao = 150,
                        data_fim = datetime(2023,5,20)
                        )
            ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Evento.query.all()


def init_app(app):
    for command in [create_db, populate, drop_db]:
        app.cli.add_command(app.cli.command()(command))
    
    @app.cli.command()
    @click.option('--name')
    @click.option('--username')
    @click.option('--email')
    @click.option('--password')
    def add_user(name, username, email,password):
        new_user = User()
        new_user.name = name
        new_user.username = username
        new_user.email = email
        new_user.password = password
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            print("Error in add user")
        