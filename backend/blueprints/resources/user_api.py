from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User
from backend.ext.base import db
from flask_mail import Message
from backend.ext.mail import mail
import random, os, string
from flasgger import swag_from

#define o blueprint de usuarios
bp_user = Blueprint('user_route', __name__, url_prefix='/api/v1/user')


def senha_radomica():
    # define o tamenho da senha
    tamanho = 12
    # carrega todos caracteres
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    # randomiza uma senha com os caracteres carregados usando o tamanho parametrizado
    nova_senha = "".join(random.choice(chars) for i in range(tamanho))
    #define a nova senha para o usuário da trazido na query
    return nova_senha

#rota para criar usuário
@bp_user.route('/create', methods=["POST"])
@swag_from('swagger/user/create.yml')
def create_user():
    novo_username = request.get_json().get("username")
    novo_name = request.get_json().get("name")
    novo_password = request.get_json().get("password")
    novo_email = request.get_json().get("email")
    if db.session.query(User).where(User.username == novo_username).first() is not None:
        return jsonify({'msg': 'Usuário já existente'}), 404
    elif db.session.query(User).where(User.email == novo_email).first() is not None:
        return jsonify({'msg':'E-mail já utilizado'}), 404
    else:
        #Valida se todos os dados foram enviados
        if novo_name is None or novo_password is None or novo_email is None or novo_username is None:
            return jsonify({"msg": "Dados incompletos"})
        novo_usuario = User()
        novo_usuario.name = novo_name
        novo_usuario.email = novo_email
        novo_usuario.password = novo_password
        novo_usuario.username = novo_username
        novo_usuario.status = True
        novo_usuario.tipo_usuario = 2
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({"msg": "usuário criado com sucesso"})

#rota para atualizar usuário
@bp_user.route("/update/<id>", methods=["PUT"])
@jwt_required()
@swag_from('swagger/user/update.yml')
def update_user(id):
    query = db.session.query(User).where(User.id == id).first()
    if query is None:
        return jsonify({"msg": "Usuário não encontrado"}), 404
    else:
        query.name = request.get_json().get("name")
        query.email = request.get_json().get("email")
        query.username = request.get_json().get("username")
        query.password = request.get_json().get("password")
        db.session.commit()
        return jsonify({"msg": "Usuário atualizado com sucesso"})

#rota para ativar usuário
@bp_user.route('/active/<id>', methods=["GET"])
@jwt_required()
@swag_from('swagger/user/active.yml')
def active_user(id):
    query = db.session.query(User).where(User.id == id).first()
    if query is None:
        return jsonify({"msg": "Usuário não encontrado"}), 404
    else:
        query.status = True
        db.session.commit()
        return jsonify({"msg": "Usuário ativado com sucesso"})

#rota para desativar usuário
@bp_user.route('/deactive/<id>', methods=["GET"])
@jwt_required()
@swag_from('swagger/user/deactive.yml')
def deactive_user(id):
    query = db.session.query(User).where(User.id == id).first()
    if query is None:
        return jsonify({"msg": "Usuário não encontrado"})
    else:
        query.status = False
        db.session.commit()
        return jsonify({"msg": "Usuário desativado com sucesso"})
    

#rota para ler usuário
@bp_user.route('/read/<id>', methods=["GET"])
@jwt_required()
@swag_from('swagger/user/read.yml')
def get_users(id):
    query = db.session.query(User).where(User.id == id).first()
    if query is None:
        return jsonify({"msg": "Usuário não encontrado"}), 404
    else:
        return jsonify({
                        "id": query.id,
                        "name": query.name,
                        "username": query.username,
                        "email": query.email
                        })


#rota para redefinição de senha
@bp_user.route('/reset_password', methods=['POST'])
@jwt_required()
@swag_from('swagger/user/reset_password.yml')
def reset_password():
    # Pega informações enviadas no json
    user_username = request.get_json().get('username')
    user_email = request.get_json().get('email')
    #consulta o user com o username
    query = db.session.query(User).where(User.username == user_username).first()
    #se exite o usuário:
    if query is not None:
        # verifica se o e-mail enviado é o mesmo contido no cadastro se nao for retorna que não pertence
        if query.email != user_email:
            return jsonify({"msg": "E-mail não pertence ao usuário"}), 404
        #se for reseta a senha para uma randomizada e envia o e-mail para o contido no cadastro
        else:
            nova_senha = senha_radomica()
            query.password = nova_senha
            #comita a alteração
            db.session.commit()
            #define a mensagem a ser enviada 
            msg = Message("New Password",
                        sender="simple.api.pp@outlook.com",
                        recipients=[query.email],
                        html=f"""
                            <h1> Nova Senha </h1> 
                            <b>{ nova_senha }</b>
                        """
                        )
            #envia a mensagem
            mail.send(msg)

        return jsonify({"msg" : "email enviado com uma nova senha enviado"}) 

