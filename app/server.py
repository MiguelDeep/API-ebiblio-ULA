import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv

from app.views.admin import admin_bp
from app.views.user import user_bp
from app.views.auth import auth_bp
from app.models.db import db
from app.models.biblioteca import (
    Admin, Computador, EmprestimoComputador, EmprestimoLivro, Entrada, Livro,
    RelatorioDiario, Usuario, datetime
)
from flask_cors import CORS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") or \
    "postgresql://biblioteca_owner:npg_bkH06nhEVewU@ep-royal-voice-a8aciqyd-pooler.eastus2.azure.neon.tech/biblioteca?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or "uma_chave_secreta_para_dev"

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

# CORS
CORS(app)

@app.route("/")
def home():
    return "Seja Bem-Vindo!"

@app.errorhandler(Exception)
def handle_exception(e):
    logging.exception("Erro interno no servidor:")
    return jsonify(error=str(e)), 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    with app.app_context():
        print("Criando tabelas...")
        db.create_all()
        print("Tabelas criadas.")

    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
