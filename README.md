> 📌 Este projeto faz parte do meu portfólio pessoal. Sinta-se à vontade para explorar, clonar e sugerir melhorias!

# Blog API com Flask

Este é um projeto de API RESTful desenvolvida com Flask que gerencia autores e postagens de blog. A autenticação é feita via JWT, garantindo segurança e controle de acesso aos endpoints.

## 🚀 Tecnologias Usadas

- Python 3.12+
- Flask 3.x
- Flask-SQLAlchemy
- JWT (PyJWT)

## 📁 Estrutura do Projeto

```
blog/
├── blog_config.py
├── blog_extensions.py
├── blog_models.py
├── blog_routes.py
├── blog_main.py
├── requirements.txt
└── README.md
```

## 🧪 Como Executar o Projeto Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/BrunoEstrela-dev/flask-blog-api.git
cd flask-blog-api
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt # Windows
pip3 install -r requirements.txt # Linux/Mac
```

### 4. Configure a variável de ambiente para senha do admin

Crie um arquivo `.env` com o seguinte conteúdo ou exporte diretamente no terminal:

```bash
export ADMIN_SENHA="sua_senha_supersegura"
```

No Windows:

```bash
set ADMIN_SENHA="sua_senha_supersegura"
```

Ou configure direto no terminal antes de rodar a aplicação.

### 5. Execute a aplicação

```bash
python blog_main.py
```

A API estará disponível em: `http://localhost:8000`

## 🔐 Autenticação

A autenticação é feita via token JWT.

- Faça uma requisição `POST` para `/login` usando basic auth com `email` e `senha`.
- O token será retornado e deverá ser incluído nos headers das próximas requisições com:  
  `x-access-token: <seu_token>`

## 🔄 Rotas Disponíveis

### POST `/login`
- Autentica um usuário e retorna um token JWT.

### GET `/`
- Lista todas as postagens.

### GET `/postagens/<id>`
- Retorna uma postagem pelo ID.

### POST `/postagens`
- Cria uma nova postagem.

### PUT `/postagens/<id>`
- Altera uma postagem.

### DELETE `/postagens/<id>`
- Exclui uma postagem.

### GET `/autores`
- Lista todos os autores.

### GET `/autores/<id>`
- Retorna um autor pelo ID.

### POST `/autores`
- Cria um novo autor (apenas admin).

### PUT `/autores/<id>`
- Altera os dados de um autor.

### DELETE `/autores/<id>`
- Exclui um autor.

## 🛠️ Desenvolvimento

O projeto é modularizado em:

- `blog_config.py`: Configurações da aplicação
- `blog_extensions.py`: Inicialização de extensões
- `blog_models.py`: Modelos de dados (ORM)
- `blog_routes.py`: Rotas e regras de negócio
- `blog_main.py`: Ponto de entrada da aplicação

---

