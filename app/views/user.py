from flask import Blueprint, request, jsonify
from models.biblioteca import Computador, Entrada, Livro, Usuario, EmprestimoLivro, EmprestimoComputador
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
    livro_id = data.get('livro_id')

    usuario = Usuario.query.get(usuario_id)
    if not usuario or not usuario.aprovado:
        return jsonify({"error": "Usuário não aprovado ou inexistente"}), 403

    emprestimo = EmprestimoLivro(
        usuario_id=usuario_id,
        livro_id=livro_id
    )
    db.session.add(emprestimo)
    db.session.commit()

    return jsonify({"message": "Empréstimo de livro solicitado com sucesso"}), 201

@user_bp.route('/usuario/emprestimos/livro', methods=['GET'])
@user_required
def listar_emprestimos_livros():
    emprestimos = EmprestimoLivro.query.all()
    resultado = [{
        "id": e.id,
        "usuario_id": e.usuario_id,
        "nome_usuario": e.usuario.nome,
        "livro_id": e.livro_id,
        "titulo_livro": e.livro.titulo,
        "status": e.status,
        "data_pedido": e.data_pedido.strftime("%Y-%m-%d %H:%M:%S")
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
    computador_id = data.get('computador_id')

    usuario = Usuario.query.get(usuario_id)
    if not usuario or not usuario.aprovado:
        return jsonify({"error": "Usuário não aprovado ou inexistente"}), 403

    emprestimo = EmprestimoComputador(
        usuario_id=usuario_id,
        computador_id=computador_id
    )
    db.session.add(emprestimo)
    db.session.commit()

    return jsonify({"message": "Empréstimo de computador solicitado com sucesso"}), 201

@user_bp.route('/usuario/emprestimos/computadores', methods=['GET'])
@user_required
def listar_emprestimos_computadores():
    emprestimos = EmprestimoComputador.query.all()
    resultado = [{
        "id": e.id,
        "usuario_id": e.usuario_id,
        "nome_usuario": e.usuario.nome,
        "computador_id": e.computador_id,
        "marca": e.computador.marca,
        "modelo": e.computador.modelo,
        "propriedades": e.computador.propriedades,
        "status": e.status,
        "data_pedido": e.data_pedido.strftime("%Y-%m-%d %H:%M:%S")
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
        "numero_estudante":usuario.numero_estudante,
        "turma": usuario.turma,
        "curso": usuario.curso,
        "tipo_usuario": usuario.tipo_usuario
    })


@user_bp.route('/usuario/confirmar_entrada', methods=['POST'])
@user_required
def confirmar_entrada():
    try:
        usuario_id = request.user_id 
        entrada = Entrada(usuario_id=usuario_id)

        db.session.add(entrada)
        db.session.commit()

        return jsonify({
            "message": "Entrada registrada com sucesso.",
            "data_entrada": entrada.data_entrada.strftime("%Y-%m-%d %H:%M:%S")
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao registrar entrada: {str(e)}"}), 500

@user_bp.route('/usuario/livros_disponiveis', methods=['GET'])
@user_required
def listar_livros_disponiveis():
    try:
        livros = Livro.query.filter(Livro.quantidade > 0).all()
        resultado = [{
            "id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "editora": livro.editora,
            "ano_publicacao": livro.ano_publicacao,
            "codigo": livro.codigo,
            "quantidade": livro.quantidade,
            "categoria": livro.categoria
        } for livro in livros]

        return jsonify({"livros_disponiveis": resultado}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar livros disponíveis: {str(e)}"}), 500


@user_bp.route('/usuario/computadores_disponiveis', methods=['GET'])
@user_required
def listar_computadores_disponiveis():
    try:
        computadores = Computador.query.filter_by(disponivel=True).all()
        resultado = [{
            "id": pc.id,
            "marca": pc.marca,
            "modelo": pc.modelo,
            "propriedades": pc.propriedades,
            "numero_serie": pc.numero_serie,
            "especificacoes": pc.especificacoes,
            "estado": pc.estado
        } for pc in computadores]

        return jsonify({"computadores_disponiveis": resultado}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar computadores disponíveis: {str(e)}"}), 500
