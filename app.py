from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/inicio')
def pagina_inicio():
    return render_template('inicio.html')


@app.route('/looks')
def looks():
    return render_template('looks.html')


@app.route('/inscricao')
def inscricao():
    return render_template('inscricao.html')


if __name__ == '__main__':
    app.run(debug=True)