from flask import Flask
from app.views.admin import admin_bp
from app.views.user import user_bp
from app.models.db import db
from app.views.auth import auth_bp   
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

CORS(app,origins="https://frontend-ebiblio.vercel.app/")

@app.route("/")
def home():
    return "Seja Bem-Vindo!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
