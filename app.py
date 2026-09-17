from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
) 
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#configurações SQLite
app.config['SECRET_KEY'] = "m@r1@n@"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///usuarios.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configuração SQLAlchemy
db = SQLAlchemy(app)

#Configuração do login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Faça login para acessar esta página."

#==================================
# MODELS
#==================================
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(12), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='usuario')

@login_manager.user_loader
def carregar_usuario(user_id):
    return db.session.get(Usuario, int(user_id))

#==================================
# PAGINA INICIAL
#==================================
@app.route('/')
def index():
    return render_template('base.html')

#==================================
# CADASTRO
#==================================
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            flash ("Este e-mail já está cadastrado.")
            return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(
            nome = nome,
            email = email,
            senha = senha_hash,
            perfil = 'usuario'
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso!")

        return redirect(url_for('login'))

    return render_template('cadastro.html')

#==================================
# LOGIN
#==================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('perfil'))

        flash("E-mail ou senha incorretos.")

    return render_template('login.html')

#==================================
# LOGOUT
#==================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.")
    return redirect(url_for('login'))