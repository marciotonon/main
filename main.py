from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from classes import db, Usuario, Categoria, Produto
from flask_login import LoginManager
from rotas import rotas_app

import os

app = Flask(__name__)
app.register_blueprint(rotas_app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios1.db'
app.config['SECRET_KEY'] = 'DeuséFieloTempoTodo'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'rotas_app.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


def create_app():
    # Verifica se o banco de dados não existe antes de criar todas as tabelas
    if not os.path.exists('usuarios.db'):
        with app.app_context():
            db.create_all()

    if not os.path.exists('categoria.db'):
        with app.app_context():
            db.create_all()

    if not os.path.exists('produto.db'):
        with app.app_context():
            db.create_all()

    return app

PRODUTOS_POR_PAGINA = 4

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
