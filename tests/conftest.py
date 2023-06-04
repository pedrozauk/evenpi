
import pytest
from backend.app import create_app
from flask import url_for
from backend.ext.base import db
from backend.ext.commands import populate


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="session")
def preenche_banco(app):
    with app.app_context():
        return populate()
    

@pytest.fixture(scope="function")
def user_autentication(client):
    """Autentica o usuário"""
    def get_jwt(username, password):
        response = client.post(
                                url_for("auth.login"),
                                json={   
                                        "username" : username,
                                        "password": password
                                
                                }                    
                                )
        return response
    return get_jwt