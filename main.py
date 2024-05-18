import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Função para verificar se o login é válido
def verificar_login(username, senha):
    try:
        with open('usuarios.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
            for usuario in usuarios:
                if usuario['username'] == username and usuario['senha'] == senha:
                    return True
    except FileNotFoundError:
        return False
    return False

# Função para verificar se um usuário já existe
def verificar_usuario_existe(username):
    try:
        with open('usuarios.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
            for usuario in usuarios:
                if usuario['username'] == username:
                    return True
    except FileNotFoundError:
        return False
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        razao_social = request.form['razao_social']
        cnpj = request.form['cnpj']
        endereco = request.form['endereco']
        numero = request.form['numero']
        estado = request.form['estado']
        bairro = request.form['bairro']
        email = request.form['email']
        telefone = request.form['telefone']
        username = request.form['username']
        senha = request.form['senha']

        if verificar_usuario_existe(username):
            return render_template('formulario_registro.html', erro="Nome de usuário já existe.")
        else:
            dados_registro = {
                "razao_social": razao_social,
                "cnpj": cnpj,
                "endereco": endereco,
                "numero": numero,
                "estado": estado,
                "bairro": bairro,
                "email": email,
                "telefone": telefone,
                "username": username,
                "senha": senha
            }

            try:
                with open('usuarios.json', 'r') as arquivo:
                    usuarios = json.load(arquivo)
            except FileNotFoundError:
                usuarios = []

            usuarios.append(dados_registro)
            with open('usuarios.json', 'w') as arquivo:
                json.dump(usuarios, arquivo)

            return redirect('/')
    else:
        return render_template('formulario_registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        if verificar_login(username, senha):
            return redirect(url_for('lista_registros'))
        else:
            return render_template('tela_login.html', erro="Nome de usuário ou senha incorretos.")
    else:
        return render_template('tela_login.html')

@app.route('/registros')
def lista_registros():
    try:
        with open('usuarios.json', 'r') as arquivo:
            registros = json.load(arquivo)
    except FileNotFoundError:
        registros = []

    return render_template('lista_registros.html', registros=registros)

if __name__ == '__main__':
    app.run(debug=True)
