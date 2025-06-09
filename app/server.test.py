"""from flask import Flask
from app.views.admin import admin_bp
from app.views.user import user_bp
from app.models.db import db
from app.models.biblioteca import Usuario, Admin, Entrada, Livro, Computador, EmprestimoLivro, EmprestimoComputador, RelatorioDiario
from flask_sqlalchemy import SQLAlchemy
from views.auth import auth_bp
from flask_cors import CORS
from dotenv import load_dotenv
import os
"""
from flask import Flask
from app.views.admin import admin_bp
from app.views.user import user_bp
from app.models.db import db
from app.models.biblioteca import Usuario, Admin, Entrada, Livro, Computador, EmprestimoLivro, EmprestimoComputador, RelatorioDiario
from flask_sqlalchemy import SQLAlchemy
from app.views.auth import auth_bp   
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///biblioteca.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://biblioteca_owner:npg_bkH06nhEVewU@ep-royal-voice-a8aciqyd-pooler.eastus2.azure.neon.tech/biblioteca?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yufjkhlj38o45940ujto34khn'
db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

SECRET_KEY = os.getenv("SECRET_KEY")
FLASK_ENV = os.getenv("FLASK_ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
CORS(app)

#, origins=["http://localhost:3000"]

@app.route("/")
def home():
    return "Seja Bem-Vindo!"



if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    
  app.run(debug=True)


#db.drop_all() --> apagar as tabelas

# quando abrir o projeto tenho de dar sempre cd "app"