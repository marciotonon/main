# classes.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import  UserMixin


db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    # Relacionamento um-para-muitos com Categoria
    categorias = db.relationship('Categoria', backref='usuario', lazy=True)

    # Relacionamento um-para-muitos com Produto
    produtos = db.relationship('Produto', backref='usuario', lazy=True)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)

    # Relacionamento muitos-para-um com Usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relacionamento um-para-muitos com Produto
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    # Relacionamento muitos-para-um com Usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relacionamento muitos-para-um com Categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
