import click
from backend.ext.base import db
from backend.models import User
def create_db():
    """ Criar o banco"""
    db.create_all()

def init_app(app):
    for command in [create_db]:
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
        