from blog_config import create_app
from blog_routes import init_routes
from blog_models import inicializar_banco

app = create_app()
init_routes(app)
inicializar_banco(app)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
