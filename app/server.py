from flask import Flask
from app.views.admin import admin_bp
from app.views.user import user_bp
from app.models.db import db
from app.views.auth import auth_bp   
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") or "postgresql://biblioteca_owner:npg_bkH06nhEVewU@ep-royal-voice-a8aciqyd-pooler.eastus2.azure.neon.tech/biblioteca?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

CORS(app,origins="https://frontend-ebiblio.vercel.app")

@app.route("/")
def home():
    return "Seja Bem-Vindo!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    debug_mode = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug_mode, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

