from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

# Configurar para servir arquivos estáticos (CSS, JS, etc.)
app.static_folder = 'static'
app.template_folder = 'templates'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

def create_app():
    # Verifica se o banco de dados não existe antes de criar todas as tabelas
    if not os.path.exists('usuarios.db'):
        with app.app_context():
            db.create_all()

    return app

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

if __name__ == '__main__':
    create_app().run(debug=True)
