from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
from functools import wraps
#from models.biblioteca import Usuario, Admin
from app.models.biblioteca import Usuario, Admin
from app.models.db import db

#from models.db import db

SECRET_KEY = 'yufjkhlj38o45940ujto34khn'
auth_bp = Blueprint('auth', __name__)

def gerar_token(user_id, tipo):
    payload = {
        'id': user_id,
        'tipo': tipo,
        'exp': datetime.now() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')  

def token_required(tipo_esperado):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]

            if not token:
                return jsonify({'mensagem': 'Token não fornecido!'}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if data['tipo'] != tipo_esperado:
                    return jsonify({'mensagem': 'Acesso negado!'}), 403
                request.user_id = data['id']
            except jwt.ExpiredSignatureError:
                return jsonify({'mensagem': 'Token expirado!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'mensagem': 'Token inválido!'}), 401

            return f(*args, **kwargs)
        return decorated
    return decorator

user_required = token_required('user')
admin_required = token_required('admin')

@auth_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email'], senha=data['senha']).first()

    if not usuario or not usuario.aprovado:
        return jsonify({'mensagem': 'Credenciais inválidas ou conta não aprovada'}), 401

    token = gerar_token(usuario.id, 'user')
    return jsonify({'token': token})

@auth_bp.route('/login/admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    admin = Admin.query.filter_by(email=data['email'], senha=data['senha']).first()

    if not admin:
        return jsonify({'mensagem': 'Credenciais inválidas admin'}), 401

    token = gerar_token(admin.id, 'admin')
    return jsonify({'token': token})



@auth_bp.route('/sair', methods=['POST'])
def logout():
    return jsonify({'mensagem': 'Logout realizado com sucesso!'}), 200
