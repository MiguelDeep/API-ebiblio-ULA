from flask import Blueprint, request, jsonify
from models.biblioteca import Usuario, EmprestimoLivro, EmprestimoComputador
from models.db import db
from .auth import user_required



user_bp = Blueprint('user', __name__)

@user_bp.route("/usuario/home")

def user_home():
    return "Painel de usuário"

@user_bp.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    numero_estudante = data.get('numero_estudante')
    senha = data.get('senha')
    turma = data.get('turma')
    curso = data.get('curso')
    tipo_usuario = data.get('tipo_usuario')

    if not nome or not email or not senha:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "Email já cadastrado"}), 409

    if Usuario.query.filter_by(numero_estudante=numero_estudante).first():
        return jsonify({"error": "Número de estudante já cadastrado"}), 409

    novo_usuario = Usuario(
        numero_estudante=numero_estudante,
        nome=nome,
        email=email,
        senha=senha,
        aprovado=False,
        turma=turma,
        curso=curso,
        tipo_usuario=tipo_usuario
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuário criado com sucesso! Aguarde aprovação do administrador.",
        "usuario": {
            "id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "email": novo_usuario.email,
            "aprovado": novo_usuario.aprovado,
            "numero_estudante": novo_usuario.numero_estudante,
            "turma": novo_usuario.turma,
            "curso": novo_usuario.curso,
            "tipo_usuario": novo_usuario.tipo_usuario
        }
    }), 201


@user_bp.route('/usuario/emprestimos/livros', methods=['POST'])
@user_required
def emprestarLivros():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    tipo_pessoa = data.get('tipo_pessoa')
    livro_id = data.get('livro_id')

    usuario = Usuario.query.get(usuario_id)
    if not usuario or not usuario.aprovado:
        return jsonify({"error": "Usuário não aprovado ou inexistente"}), 403

    emprestimo = EmprestimoLivro(
        usuario_id=usuario_id,
        tipo_pessoa=tipo_pessoa,
        livro_id=livro_id
    )
    db.session.add(emprestimo)
    db.session.commit()

    return jsonify({"message": "Empréstimo de livro solicitado com sucesso"}), 201

@user_bp.route('/usuario/emprestimos/livro', methods=['GET'])
@user_required
def ListareLivrosEmprestar():
    emprestimos = EmprestimoLivro.query.all()
    resultado = [{
        "id": e.id,
        "usuario_id": e.usuario_id,
        "livro_id": e.livro_id,
        "status": e.status
    } for e in emprestimos]
    return jsonify(resultado), 200

@user_bp.route('/usuario/emprestimos/livro/<int:id>', methods=['PUT'])
@user_required
def ActualizarLivrosEmprestar(id):
    emprestimo = EmprestimoLivro.query.get(id)
    if not emprestimo:
        return jsonify({"error": "Empréstimo não encontrado"}), 404

    data = request.get_json()
    emprestimo.status = data.get('status', emprestimo.status)

    db.session.commit()
    return jsonify({"message": "Empréstimo de livro atualizado com sucesso"}), 200

@user_bp.route('/usuario/emprestimos/livro/<int:id>', methods=['DELETE'])
@user_required
def ApagarLivrosEmprestar(id):
    emprestimo = EmprestimoLivro.query.get(id)
    if not emprestimo:
        return jsonify({"error": "Empréstimo não encontrado"}), 404

    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({"message": "Empréstimo de livro excluído com sucesso"}), 200


@user_bp.route('/usuario/emprestimos/computadores', methods=['POST'])
@user_required
def CriarComputadorEmprestar():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    tipo_pessoa = data.get('tipo_pessoa')
    computador_id = data.get('computador_id')

    usuario = Usuario.query.get(usuario_id)
    if not usuario or not usuario.aprovado:
        return jsonify({"error": "Usuário não aprovado ou inexistente"}), 403

    emprestimo = EmprestimoComputador(
        usuario_id=usuario_id,
        tipo_pessoa=tipo_pessoa,
        computador_id=computador_id
    )
    db.session.add(emprestimo)
    db.session.commit()

    return jsonify({"message": "Empréstimo de computador solicitado com sucesso"}), 201

@user_bp.route('/usuario/emprestimos/computadores', methods=['GET'])
@user_required
def ListarComputadorEmprestar():
    emprestimos = EmprestimoComputador.query.all()
    resultado = [{
        "id": e.id,
        "usuario_id": e.usuario_id,
        "computador_id": e.computador_id,
        "status": e.status
    } for e in emprestimos]
    return jsonify(resultado), 200

@user_bp.route('/usuario/emprestimos/computadores/<int:id>', methods=['PUT'])
@user_required
def ActualizarComputadorEmprestar(id):
    emprestimo = EmprestimoComputador.query.get(id)
    if not emprestimo:
        return jsonify({"error": "Empréstimo não encontrado"}), 404

    data = request.get_json()
    emprestimo.status = data.get('status', emprestimo.status)

    db.session.commit()
    return jsonify({"message": "Empréstimo de computador atualizado com sucesso"}), 200

@user_bp.route('/usuario/emprestimos/computadores/<int:id>', methods=['DELETE'])
@user_required
def ApagarComputadorEmprestar(id):
    emprestimo = EmprestimoComputador.query.get(id)
    if not emprestimo:
        return jsonify({"error": "Empréstimo não encontrado"}), 404

    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({"message": "Empréstimo de computador excluído com sucesso"}), 200



@user_bp.route('/usuario/perfil')
@user_required
def perfil():
    usuario = Usuario.query.get(request.user_id)
    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "numero_estudante":usuario.numero_estudante
    })
