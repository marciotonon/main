from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from classes import db, Usuario, Categoria, Produto
from flask_paginate import Pagination, get_page_args


import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SECRET_KEY'] = 'DeuséFieloTempoTodo'
db.init_app(app)

# Configurar para servir arquivos estáticos (CSS, JS, etc.)
app.static_folder = 'static'
app.template_folder = 'templates'

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

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('login.html', usuarios=usuarios)

@app.route('/new')
def new():
    usuarios = Usuario.query.all()
    return render_template('cadastrar.html', usuarios=usuarios)


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if usuario:
            return render_template('home.html', usuario=usuario)

    return render_template('login.html')

#rotas produtos
@app.route('/listaprodutos')
def produtos():
    # Configurando a paginação
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Defina o número desejado de itens por página

    # Obtendo a lista de produtos paginada
    produtos_paginados = Produto.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('listaprodutos.html', produtos_paginados=produtos_paginados)

@app.route('/new_produto')
def new_produto():
    categorias = Categoria.query.all()
    return render_template('cadastrar_produto.html', categorias=categorias)

# Adicione esta rota para excluir uma categoria
@app.route('/delete_produto/<int:produto_id>', methods=['GET', 'POST'])
def delete_produto(produto_id):
    # Obtém a categoria pelo ID
    produto = Produto.query.get(produto_id)

    # Verifica se a categoria existe
    if produto:
        # Remove a categoria do banco de dados
        db.session.delete(produto)
        db.session.commit()

        flash('Produto excluída com sucesso.', 'success')  # Mensagem de sucesso
    else:
        flash('Produto não encontrada.', 'error')  # Mensagem de erro

    return redirect(url_for('produtos'))

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form['nome']
    preco = request.form['preco']
    categoria_id = request.form['categoria']  # Obtém a categoria selecionada

    # Obtém a categoria pelo ID
    categoria = Categoria.query.get(categoria_id)

    if categoria:
        novo_produto = Produto(nome=nome, preco=preco, categoria=categoria)
        db.session.add(novo_produto)
        db.session.commit()

        flash('Produto cadastrado com sucesso.', 'success')
    else:
        flash('Categoria não encontrada.', 'error')

    return redirect(url_for('produtos'))


# Adicione esta rota para excluir uma categoria
@app.route('/delete_categoria/<int:categoria_id>', methods=['GET', 'POST'])
def delete_categoria(categoria_id):
    # Obtém a categoria pelo ID
    categoria = Categoria.query.get(categoria_id)

    # Verifica se a categoria existe
    if categoria:
        # Remove a categoria do banco de dados
        db.session.delete(categoria)
        db.session.commit()

        flash('Categoria excluída com sucesso.', 'success')  # Mensagem de sucesso
    else:
        flash('Categoria não encontrada.', 'error')  # Mensagem de erro

    return redirect(url_for('categorias'))


# Suas rotas categoria existentes
@app.route('/listacategoria')
def categorias():
    categorias = Categoria.query.all()
    return render_template('listaCategoria.html', categorias=categorias)

@app.route('/new_categoria')
def new_categoria():
    return render_template('cadastrar_categoria.html')

@app.route('/cadastrar_categoria', methods=['GET', 'POST'])
def cadastrar_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        # Verificar se a categoria já existe pelo nome e descrição
        categoria_existente = Categoria.query.filter_by(nome=nome, descricao=descricao).first()

        if categoria_existente:
            flash('Categoria já existe.', 'error')  # Mensagem de erro
            return render_template('cadastrar_categoria.html')

        # Se não existir, criar a nova categoria
        novo_categoria = Categoria(nome=nome, descricao=descricao)
        db.session.add(novo_categoria)
        db.session.commit()

        flash('Categoria cadastrada com sucesso.', 'success')  # Mensagem de sucesso

        return redirect(url_for('categorias'))

    # Tratar o método GET aqui (se necessário)
    return render_template('cadastrar_categoria.html')

if __name__ == '__main__':
    create_app().run(debug=True)
