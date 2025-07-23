from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from blog_extensions import db
import os


# Definir a estrutura da tabela Postagem. Toda postagem deve conter um id_postagem, um titulo e um autor


class Postagem(db.Model):
    __tablename__ = "postagem"
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)

# Relacionamento de uma postagem com o autor (Para isso deve-se utilizar no campo ForeignKey o seguinte formato: nome da tabela.nome da propriedade)
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))

    autor = db.relationship("Autor", back_populates="postagens")

# Ter campos como criado_em e atualizado_em permite rastrear a criação e alteração de registros.
    criado_em = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    alterado_em = db.Column(db.DateTime, default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))

# Método especial do Python que serve para retornar uma representação textual "oficial" de um objeto — geralmente usada para debug.
    def __repr__(self):
        return f"<Postagem id={self.id_postagem} titulo='{self.titulo}'>"

# Definir a estrutura da tabela Autor. Todo autor deve conter um id_autor, um email, uma senha, se ele é admin e quais postagens foram realizadas


class Autor(db.Model):
    __tablename__ = "autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)


# Ter campos como criado_em e atualizado_em permite rastrear a criação e alteração de registros.
    criado_em = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    alterado_em = db.Column(db.DateTime, default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))


# Um autor pode ter feito várias postagens. Para criar esse relacionamento é necessário passar o nome da classe no campo relationship
    postagens = db.relationship("Postagem", back_populates="autor")


# Método especial do Python que serve para retornar uma representação textual "oficial" de um objeto — geralmente usada para debug.

    def __repr__(self):
        return f"<Autor id={self.id_autor} nome='{self.nome}'>"


# Inicializar banco de dados


def inicializar_banco(app):

    # executa o comando para criar o banco de dados
    with app.app_context():
        db.drop_all()  # Este comando apaga qualquer estrutura prévia que possa existir
        db.create_all()  # Este comando permie criar todas as tabelas que estão anexadas ao db

# Como estamos executando esses comandos para criar a estrutura incial do nosso banco de dados é importante aproveitar esse momento para criar também os nossos usuários administradores

        senha = os.getenv("ADMIN_SENHA")
        if not senha:
            raise ValueError("ADMIN_SENHA não definida no ambiente.")
    # Este comando cria usuários administradores
        autor = Autor(
            nome="Bruno",
            email="bruno@gmail.com",
            senha_hash=generate_password_hash(senha),
            admin=True
        )

        # Este comando adiciona um autor ao banco de dados
        db.session.add(autor)
        db.session.commit()  # Este comando salva os dados no banco de dados


# Para a função apenas ser chamada quando eu quiser
if __name__ == "__main__":
    inicializar_banco()
