from flask import Flask
from blog_extensions import db
import os

# Caminho absoluto da pasta onde este arquivo está localizado. O basedir faz com que esse sempre seja o caminho real da pasta onde o script está.
basedir = os.path.abspath(os.path.dirname(__file__))


# Criar uma API Flask


def create_app():
    app = Flask(__name__)

    # Configurações básicas
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'blog.db')}"

    # Inicializa o banco de dados com a app
    db.init_app(app)

    return app
