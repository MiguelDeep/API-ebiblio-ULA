from flask import Blueprint, request, jsonify
from .auth import admin_required
from .auth import user_required
#from models.biblioteca import Admin, Entrada,Usuario, Livro, Computador, EmprestimoLivro, EmprestimoComputador, RelatorioDiario
from app.models.biblioteca import Admin, Entrada, Usuario, Livro, Computador, EmprestimoLivro, EmprestimoComputador, RelatorioDiario

from models.db import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin")
@admin_required
def admin_home():
    return "Painel de administração"



@admin_bp.route('/admin/criar_administrador', methods=['POST'])
def criaAdmin():
    data = request.get_json()

    if not data or not data.get('nome') or not data.get('email') or not data.get('senha'):
        return jsonify({"message": "Dados incompletos."}), 400

    admin = Admin(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'], 
        criado_em=datetime.now()
    )

    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Administrador criado com sucesso!"}), 201


@admin_bp.route('/admin/emprestimos/livros/<int:id>/aprovar', methods=['PATCH'])
@admin_required
def emprestimoLivrosAprovar(id):
    emprestimo = EmprestimoLivro.query.get(id)
    if emprestimo:
        emprestimo.status = 'aprovado'
        db.session.commit()
        return jsonify({"message": "Empréstimo de livro aprovado com sucesso!"}), 200
    return jsonify({"message": "Empréstimo de livro não encontrado."}), 404


@admin_bp.route('/admin/emprestimos/livros/<int:id>/recusar', methods=['PATCH'])
@admin_required
def emprestimoLivrosReprovar(id):
    emprestimo = EmprestimoLivro.query.get(id)
    if emprestimo:
        emprestimo.status = 'recusado'
        db.session.commit()
        return jsonify({"message": "Empréstimo de livro recusado."}), 200
    return jsonify({"message": "Empréstimo de livro não encontrado."}), 404

@admin_bp.route('/admin/emprestimos/computadores/<int:id>/aprovar', methods=['PATCH'])
@admin_required
def emprestimoComputadoresAprovar(id):
    emprestimo = EmprestimoComputador.query.get(id)
    if emprestimo:
        emprestimo.status = 'aprovado'
        db.session.commit()
        return jsonify({"message": "Empréstimo de computador aprovado com sucesso!"}), 200
    return jsonify({"message": "Empréstimo de computador não encontrado."}), 404

@admin_bp.route('/admin/emprestimos/computadores/<int:id>/recusar', methods=['PATCH'])
@admin_required
def emprestimoComputadoresReprovar(id):
    emprestimo = EmprestimoComputador.query.get(id)
    if emprestimo:
        emprestimo.status = 'recusado'
        db.session.commit()
        return jsonify({"message": "Empréstimo de computador recusado."}), 200
    return jsonify({"message": "Empréstimo de computador não encontrado."}), 404


@admin_bp.route('/admin/livros', methods=['POST'])
@admin_required
def criaLivros():
    data = request.get_json()

    if not data or not data.get('titulo') or not data.get('codigo'):
        return jsonify({"message": "Dados incompletos."}), 400

    livro = Livro(
        titulo=data['titulo'],
        autor=data.get('autor'),
        editora=data.get('editora'),
        ano_publicacao=data.get('ano_publicacao'),
        codigo=data['codigo'],
        quantidade=data.get('quantidade', 0),
        categoria=data.get('categoria')
    )

    db.session.add(livro)
    db.session.commit()

    return jsonify({"message": "Livro criado com sucesso!"}), 201

@admin_bp.route('/admin/livros', methods=['GET'])
@admin_required
def ListarLivros():
    livros = Livro.query.all()
    livros_list = [{"id": livro.id, "titulo": livro.titulo, "autor": livro.autor,"editora":livro.editora ,"ano_publicacao":livro.ano_publicacao,"codigo":livro.codigo,"quantidade":livro.quantidade,"categoria":livro.categoria} for livro in livros]
    return jsonify(livros_list), 200



@admin_bp.route('/admin/livros/<int:id>', methods=['DELETE'])
@admin_required
def ApagarLivros(id):
    livro = Livro.query.get(id)
    if livro:
        db.session.delete(livro)
        db.session.commit()
        return jsonify({"message": "Livro apagado com sucesso!"}), 200
    return jsonify({"message": "Livro não encontrado."}), 404

@admin_bp.route('/admin/livros/<int:id>', methods=['PUT'])
@admin_required
def ActualizarLivros(id):
    data = request.get_json()
    livro = Livro.query.get(id)

    if livro:
        livro.titulo = data.get('titulo', livro.titulo)
        livro.autor = data.get('autor', livro.autor)
        livro.editora = data.get('editora', livro.editora)
        livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)
        livro.codigo = data.get('codigo', livro.codigo)
        livro.quantidade = data.get('quantidade', livro.quantidade)
        livro.categoria = data.get('categoria', livro.categoria)

        db.session.commit()
        return jsonify({"message": "Livro atualizado com sucesso!"}), 200

    return jsonify({"message": "Livro não encontrado."}), 404


@admin_bp.route('/admin/computadores', methods=['POST'])
@admin_required
def criarComputadores():
    data = request.get_json()

    if not data or not data.get('marca') or not data.get('numero_serie'):
        return jsonify({"message": "Dados incompletos."}), 400

    computador = Computador(
        marca=data['marca'],
        modelo=data.get('modelo'),
        propriedades=data['propriedades'],
        numero_serie=data['numero_serie'],
        especificacoes=data.get('especificacoes'),
        estado=data.get('estado', 'novo'),
        disponivel=data.get('disponivel', True)
    )

    db.session.add(computador)
    db.session.commit()

    return jsonify({"message": "Computador criado com sucesso!"}), 201

@admin_bp.route('/admin/computadores', methods=['GET'])
@admin_required
def ListarComputadores():
    computadores = Computador.query.all()
    computadores_list = [{"id": computador.id, "marca": computador.marca, "modelo": computador.modelo,"propriedades":computador.propriedades,"numero_serie":computador.numero_serie,"especificacoes":computador.especificacoes,"estado":computador.estado,"disponivel":computador.disponivel} for computador in computadores]
    return jsonify(computadores_list), 200

@admin_bp.route('/admin/computadores/<int:id>', methods=['DELETE'])
@admin_required
def apagarComputadores(id):
    computador = Computador.query.get(id)
    if computador:
        db.session.delete(computador)
        db.session.commit()
        return jsonify({"message": "Computador apagado com sucesso!"}), 200
    return jsonify({"message": "Computador não encontrado."}), 404

@admin_bp.route('/admin/computadores/<int:id>', methods=['PUT'])
@admin_required
def ActualizarComputadores(id):
    data = request.get_json()
    computador = Computador.query.get(id)

    if computador:
        computador.marca = data.get('marca', computador.marca)
        computador.modelo = data.get('modelo', computador.modelo)
        computador.propriedades = data.get('propriedades', computador.propriedades)
        computador.numero_serie = data.get('numero_serie', computador.numero_serie)
        computador.especificacoes = data.get('especificacoes', computador.especificacoes)
        computador.estado = data.get('estado', computador.estado)
        computador.disponivel = data.get('disponivel', computador.disponivel)

        db.session.commit()
        return jsonify({"message": "Computador atualizado com sucesso!"}), 200

    return jsonify({"message": "Computador não encontrado."}), 404


@admin_bp.route('/admin/relatorios/diario', methods=['GET'])
@admin_required
def verRelatorio():
    total_usuarios = Usuario.query.count()
    
    total_emprestimos_livros = EmprestimoLivro.query.count()
    
    total_emprestimos_computadores = EmprestimoComputador.query.count()
    
    total_livros = Livro.query.count()

    from sqlalchemy import func

    top_usuarios_livros = (
        db.session.query(Usuario.nome, func.count(EmprestimoLivro.id).label('total_emprestimos'))
        .join(EmprestimoLivro)
        .group_by(Usuario.id)
        .order_by(func.count(EmprestimoLivro.id).desc())
        .limit(3)
        .all()
    )

    top_usuarios_computadores = (
        db.session.query(Usuario.nome, func.count(EmprestimoComputador.id).label('total_emprestimos'))
        .join(EmprestimoComputador)
        .group_by(Usuario.id)
        .order_by(func.count(EmprestimoComputador.id).desc())
        .limit(3)
        .all()
    )

    from collections import defaultdict
    emprestimos_por_usuario = defaultdict(int)
    for nome, total in top_usuarios_livros:
        emprestimos_por_usuario[nome] += total
    for nome, total in top_usuarios_computadores:
        emprestimos_por_usuario[nome] += total

    top_usuarios = sorted(emprestimos_por_usuario.items(), key=lambda x: x[1], reverse=True)[:3]

    top_usuarios_list = [{"nome": nome, "total_emprestimos": total} for nome, total in top_usuarios]

    relatorio = RelatorioDiario(
        data_relatorio=datetime.now(),
        total_entradas=total_usuarios,
        total_emprestimos_livros=total_emprestimos_livros,
        total_emprestimos_computadores=total_emprestimos_computadores,
        total_livros=total_livros
    )
    db.session.add(relatorio)
    db.session.commit()

    return jsonify({
        "data_relatorio": relatorio.data_relatorio.strftime("%Y-%m-%d %H:%M:%S"),
        "total_usuarios": total_usuarios,
        "total_emprestimos_livros": total_emprestimos_livros,
        "total_emprestimos_computadores": total_emprestimos_computadores,
        "total_livros": total_livros,
        "top_usuarios_emprestimos": top_usuarios_list
    }), 200



@admin_bp.route('/admin/usuarios/pendentes', methods=['GET'])
@admin_required
def listar_usuarios_pendentes():
    pendentes = Usuario.query.filter_by(aprovado=False).all()
    
    resultado = []
    for user in pendentes:
        resultado.append({
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "numero_estudante": user.numero_estudante,
            "aprovacao":user.aprovado,
            "criado_em": user.criado_em.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(resultado), 200


@admin_bp.route('/admin/aprovar_usuario/<int:user_id>', methods=['PUT'])
@admin_required
def aprovar_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    
    if not usuario:
        return jsonify({"mensagem": "Usuário não encontrado."}), 404
    if usuario.aprovado:
        return jsonify({"mensagem": "Usuário já está aprovado."}), 400

    usuario.aprovado = True
    db.session.commit()

    return jsonify({"mensagem": f"Usuário '{usuario.nome}' aprovado com sucesso."}), 200


@admin_bp.route('/admin/usuarios', methods=['GET'])
@admin_required
def ver_usuarios():
    usuarios = Usuario.query.all()
    usuarios_list = [{"id":usuario.id,"numero_estudante": usuario.numero_estudante, "nome": usuario.nome, "email":usuario.email,"estado":usuario.aprovado} for usuario in usuarios]
    return jsonify(usuarios_list), 200

@admin_bp.route('/admin/emprestimos/pendentes', methods=['GET'])
@admin_required
def listar_emprestimos_pendentes():
    livros_pendentes = EmprestimoLivro.query.filter_by(status='pendente').all()
    livros_data = []
    for emp in livros_pendentes:
        livros_data.append({
            "id": emp.id,
            "tipo": "livro",
            "usuario": emp.usuario.nome,
            "livro": emp.livro.titulo,
            "data_pedido": emp.data_pedido.strftime('%Y-%m-%d %H:%M:%S'),
            "status": emp.status
        })

    computadores_pendentes = EmprestimoComputador.query.filter_by(status='pendente').all()
    computadores_data = []
    for emp in computadores_pendentes:
        computadores_data.append({
            "id": emp.id,
            "tipo": "computador",
            "usuario": emp.usuario.nome,
            "computador": f"{emp.computador.marca} - {emp.computador.modelo}",
            "data_pedido": emp.data_pedido.strftime('%Y-%m-%d %H:%M:%S'),
            "status": emp.status
        })

    emprestimos_pendentes = livros_data + computadores_data

    return jsonify(emprestimos_pendentes), 200


@admin_bp.route('/admin/entradas', methods=['GET'])
@admin_required
def listar_entradas():
    entradas = Entrada.query.all()

    resultado = [{
        "id": entrada.id,
        "data_entrada": entrada.data_entrada.strftime("%Y-%m-%d %H:%M:%S"),
        "nome": entrada.usuario.nome,
        "email": entrada.usuario.email,
        "numero_estudante": entrada.usuario.numero_estudante,
        "turma": entrada.usuario.turma,
        "curso": entrada.usuario.curso,
        "tipo_usuario": entrada.usuario.tipo_usuario
    } for entrada in entradas]

    return jsonify(resultado), 200
