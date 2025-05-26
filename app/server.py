from flask import Flask
from views.admin import admin_bp
from views.user import user_bp
from models.db import db
from models.biblioteca import Usuario, Admin, Entrada, Livro, Computador, EmprestimoLivro, EmprestimoComputador, RelatorioDiario
from flask_sqlalchemy import SQLAlchemy
from views.auth import auth_bp
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()




server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///biblioteca.db"
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SECRET_KEY'] = 'yufjkhlj38o45940ujto34khn'
db.init_app(server)

server.register_blueprint(auth_bp)
server.register_blueprint(admin_bp)
server.register_blueprint(user_bp)

SECRET_KEY = os.getenv("SECRET_KEY")
FLASK_ENV = os.getenv("FLASK_ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
CORS(server)

#, origins=["http://localhost:3000"]

@server.route("/")
def home():
    return "Seja Bem-Vindo!"



if __name__ == "__main__":
  with server.app_context():
    db.create_all()
    
  server.run(debug=True)


#db.drop_all() --> apagar as tabelas

# quando abrir o projeto tenho de dar sempre cd "app"