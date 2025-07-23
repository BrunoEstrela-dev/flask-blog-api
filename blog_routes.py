from flask import Flask, jsonify, request, make_response
from blog_models import Autor, Postagem, db
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt


def init_routes(app):

    # Decorator para verificar se o token de acesso foi enviado e é válido
    def token_obrigatorio(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            # Verifica se um token foi enviado
            if "x-access-token" in request.headers:
                token = request.headers["x-access-token"]

            if not token:
                return jsonify({"erro": "Token não foi incluído."}), 401

            # Se temos um token -> validar acesso consultando o BD
            try:
                resultado = jwt.decode(
                    token, app.config["SECRET_KEY"], algorithms=["HS256"]
                )
                autor_autenticado = Autor.query.filter_by(
                    id_autor=resultado["id_autor"]
                ).first()
                if not autor_autenticado:
                    return jsonify({"erro": "Usuário não encontrado."}), 401
            except ExpiredSignatureError:
                return jsonify({"erro": "Token expirado. Faça login novamente."}), 401
            except InvalidTokenError:
                return jsonify({"erro": "Token inválido ou corrompido."}), 401

            return f(autor_autenticado, *args, **kwargs)

        return decorated


# === ROTA DE LOGIN ===


    @app.route("/login", methods=["POST"])
    def login():

        # Extrai as informações que foram passadas de autenticação na nossa API (No nosso caso serão e-mail e senha)
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            resposta = make_response("erro: E-mail ou senha inválidos.", 401)
            resposta.headers["WWW-Authenticate"] = "basic realm='Login requerido.'"
            return resposta

        autor_autenticado = Autor.query.filter_by(email=auth.username).first()
        if not autor_autenticado or not check_password_hash(autor_autenticado.senha_hash, auth.password):
            resposta = make_response("erro: E-mail ou senha inválidos.", 401)
            resposta.headers["WWW-Authenticate"] = "basic realm='Login requrido.'"
            return resposta

        token = jwt.encode(
            {
                "id_autor": autor_autenticado.id_autor,

                # A partir de versões mais recentes do Python (>=3.12), datetime.utcnow() está deprecated (obsoleto), pois ele retorna um datetime sem informação de fuso horário. Isso pode causar problemas ao comparar com objetos "timezone-aware". Por isso deve-se utilizar datetime.now(timezone.utc) importando timezone da biblioteca datetime.
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            app.config["SECRET_KEY"]
        )

        return jsonify({"token": token}), 200


# === ROTA INICIAL (listar postagens) ===

    @app.route("/")
    @token_obrigatorio
    def obter_postagens(autor):
        postagens = Postagem.query.all()

        lista = [
            {
                "titulo": p.titulo,
                "id_autor": p.id_autor
            }
            for p in postagens
        ]
        return jsonify({"postagens": lista})


# === Obter postagem por ID ===

    @app.route("/postagens/<int:id_postagem>", methods=["GET"])
    @token_obrigatorio
    def obter_postagens_por_id(autor, id_postagem):
        postagem = Postagem.query.get(id_postagem)
        if not postagem:
            return jsonify({"erro": "Postagem não encontrada."}), 404

        return jsonify({
            "postagens": {
                "titulo": postagem.titulo,
                "id_autor": postagem.id_autor
            }
        })


# === Criar nova postagem ===

    @app.route("/postagens", methods=["POST"])
    @token_obrigatorio
    def nova_postagem(autor):
        dados = request.get_json()
        if "titulo" not in dados:
            return jsonify({"erro": "O campo 'titulo' é obrigatório."}), 400

        postagem = Postagem(
            titulo=dados["titulo"],
            id_autor=autor.id_autor
        )

        db.session.add(postagem)
        db.session.commit()

        return jsonify({
            "mensagem": "Postagem criada com sucesso!",
            "id_postagem": postagem.id_postagem
        }), 201


# === Alterar postagem ===

    @app.route("/postagens/<int:id_postagem>", methods=["PUT"])
    @token_obrigatorio
    def alterar_postagens(autor, id_postagem):
        dados = request.get_json()
        postagem = Postagem.query.get(id_postagem)

        if not postagem:
            return jsonify({"erro": "Postagem não encontrada."}), 404
        if postagem.id_autor != autor.id_autor:
            return jsonify({"erro": "Sem permissão para alterar esta postagem."}), 403

        if "titulo" in dados:
            postagem.titulo = dados["titulo"]

        db.session.commit()
        return jsonify({"mensagem": "Postagem alterada com sucesso!"}), 200


# === Excluir postagem ===

    @app.route("/postagens/<int:id_postagem>", methods=["DELETE"])
    @token_obrigatorio
    def excluir_postagens(autor, id_postagem):
        postagem = Postagem.query.get(id_postagem)
        if not postagem:
            return jsonify({"erro": "Postagem não encontrada."}), 404
        if postagem.id_autor != autor.id_autor:
            return jsonify({"erro": "Sem permissão para excluir esta postagem."}), 403

        db.session.delete(postagem)
        db.session.commit()

        return jsonify({"mensagem": f"A postagem '{postagem.titulo}' foi excluída com sucesso!"}), 200


# === Listar autores ===

    @app.route("/autores", methods=["GET"])
    @token_obrigatorio
    def obter_autores(autor):
        # Busca todos os autores no banco de dados e armazena em uma variável
        autores = Autor.query.all()

        lista = [
            {
                "id_autor": a.id_autor,
                "nome": a.nome,
                "email": a.email
            }
            for a in autores
        ]
        return jsonify({"autores": lista})


# === Obter autor por ID ===


    @app.route("/autores/<int:id_autor>", methods=["GET"])
    @token_obrigatorio
    def obter_autor_por_id(autor, id_autor):
        autor_db = Autor.query.get(id_autor)

        if not autor_db:
            return jsonify({"erro": "Autor não encontrado."}), 404

        return jsonify({
            "autor": {
                "id_autor": autor_db.id_autor,
                "nome": autor_db.nome,
                "email": autor_db.email
            }
        })


# === Criar novo autor ===

    @app.route("/autores", methods=["POST"])
    @token_obrigatorio
    def criar_autor(autor):
        if not autor.admin:
            return jsonify({"erro": "Sem permissão para criar autores."}), 403

        dados = request.get_json()
        if not all(k in dados for k in ("nome", "email", "senha")):
            return jsonify({"erro": "Campos obrigatórios: nome, email e senha."}), 400

        if Autor.query.filter_by(email=dados["email"]).first():
            return jsonify({"erro": "E-mail já cadastrado"}), 400

        novo_autor = Autor(
            nome=dados["nome"],
            email=dados["email"],
            senha_hash=generate_password_hash(dados["senha"])
        )

        db.session.add(novo_autor)
        db.session.commit()

        return jsonify({"mensagem": "Autor criado com sucesso!"}), 201


# === Alterar autor ===


    @app.route("/autores/<int:id_autor>", methods=["PUT"])
    @token_obrigatorio
    def alterar_autor(autor, id_autor):
        if autor.id_autor != id_autor and not autor.admin:
            return jsonify({"erro": "Sem permissão para alterar este autor."}), 403

        dados = request.get_json()
        autor_db = Autor.query.get(id_autor)
        if not autor_db:
            return jsonify({"erro": "Autor não encontrado."}), 404

        if "nome" in dados:
            autor_db.nome = dados["nome"]
        if "email" in dados:
            email_existente = Autor.query.filter_by(
                email=dados["email"]).first()
            if email_existente and email_existente.id_autor != id_autor:
                return jsonify({"erro": "E-mail já em uso por outro autor."}), 400
            autor_db.email = dados["email"]
        if "senha" in dados:
            autor_db.senha_hash = generate_password_hash(
                dados["senha"])

        db.session.commit()
        return jsonify({"mensagem": "Autor alterado com sucesso!"}), 200


# === Excluir autor ===


    @app.route("/autores/<int:id_autor>", methods=["DELETE"])
    @token_obrigatorio
    def excluir_autor(autor, id_autor):
        if autor.id_autor != id_autor and not autor.admin:
            return jsonify({"erro": "Sem permissão para excluir este autor."}), 403

        autor_db = Autor.query.get(id_autor)
        if not autor_db:
            return jsonify({"erro": "Autor não encontrado."}), 404

        db.session.delete(autor_db)
        db.session.commit()

        return jsonify({"mensagem": "Autor excluído com sucesso!"}), 200
