from .db import db
from datetime import datetime




class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    numero_estudante = db.Column(db.Integer, unique=True, nullable=False) 
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    aprovado = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    entradas = db.relationship('Entrada', backref='usuario', cascade="all, delete-orphan")
    emprestimos_livros = db.relationship('EmprestimoLivro', backref='usuario', cascade="all, delete-orphan")
    emprestimos_computadores = db.relationship('EmprestimoComputador', backref='usuario', cascade="all, delete-orphan")

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)

class Entrada(db.Model):
    __tablename__ = 'entradas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_pessoa = db.Column(db.String(20), nullable=False)
    data_entrada = db.Column(db.DateTime, default=datetime.now)
    

class Livro(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255))
    editora = db.Column(db.String(255))
    ano_publicacao = db.Column(db.Integer)
    codigo = db.Column(db.String(20), unique=True)
    quantidade = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime, default=datetime.now)

    emprestimos = db.relationship('EmprestimoLivro', backref='livro', cascade="all, delete-orphan")

class Computador(db.Model):
    __tablename__ = 'computadores'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    propriedades = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(100))
    especificacoes = db.Column(db.Text)
    estado = db.Column(db.String(50))
    disponivel = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    emprestimos = db.relationship('EmprestimoComputador', backref='computador', cascade="all, delete-orphan")

class EmprestimoLivro(db.Model):
    __tablename__ = 'emprestimos_livros'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_pessoa = db.Column(db.String(20), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='pendente')

class EmprestimoComputador(db.Model):
    __tablename__ = 'emprestimos_computadores'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_pessoa = db.Column(db.String(20), nullable=False)
    computador_id = db.Column(db.Integer, db.ForeignKey('computadores.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='pendente')

class RelatorioDiario(db.Model):
    __tablename__ = 'relatorios_diarios'

    id = db.Column(db.Integer, primary_key=True)
    data_relatorio = db.Column(db.Date, unique=True, nullable=False)
    total_entradas = db.Column(db.Integer, default=0)
    total_emprestimos_livros = db.Column(db.Integer, default=0)
    total_emprestimos_computadores = db.Column(db.Integer, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.now)
