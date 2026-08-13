import click
from flask import Flask, render_template

from config import Config
from database import close_db, init_db
from routes import api
from seed import seed_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(api)

    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        click.echo("Banco de dados inicializado.")

    @app.cli.command("seed-db")
    def seed_db_command():
        try:
            resultado = seed_db()
        except ValueError as erro:
            raise click.ClickException(str(erro)) from erro

        click.echo(
            f"{resultado['materiais']} materiais e "
            f"{resultado['movimentacoes']} movimentações "
            "cadastrados."
        )

    @app.get("/")
    @app.get("/index.html")
    def index():
        return render_template("index.html")

    @app.get("/materiais.html")
    def materiais():
        return render_template("materiais.html")

    @app.get("/entrada.html")
    def entrada():
        return render_template("entrada.html")

    @app.get("/saida.html")
    def saida():
        return render_template("saida.html")

    @app.get("/estoque.html")
    def estoque():
        return render_template("estoque.html")

    @app.get("/historico.html")
    def historico():
        return render_template("historico.html")

    return app


app = create_app()
