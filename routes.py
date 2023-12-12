# rotas.py
from flask import render_template, request, redirect, url_for, flash
from classes import db, Usuario, Produto, Categoria  # Importe o app e o db do módulo principal
from main import app
from flask import flash

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
@app.route('/produtos')
def produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/new_produto')
def new_produto():
    return render_template('cadastrar_produto.html')

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form['nome']
    preco = request.form['preco']

    novo_produto = Produto(nome=nome, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()

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