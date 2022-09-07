from flask import Flask, render_template, redirect, request, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'aonainfinnBFNFOANOnasfononfsa'


# Configurações do banco de dados
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Rota da página inicial
@app.route('/')
def index():
    if 'cpf' in session: #Verificando se a pessoa já está logada
        return redirect(url_for(home))
    return render_template('index.html')

# Rota da página de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        cliente = request.form #Armazena todos os dados inseridos no formulário em uma variável tipo dicionário
        return redirect(url_for('login'))
        '''
        ==========Possível inserção usando arquivo .py do modelo==========
        if modelo.validação(nome, senha):
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
        
        '''
    else:
        return render_template('cadastro.html')

# Rota da página de login
@app.route('/login', methods=['POST', 'GET']) #Colocando os metodos HTTP que serão usados
def login():
    if request.method == 'POST': #Se a pessoa apertar o botão 'ENTRAR' do forms
        nome = request.form['nome'] #Adicionando a uma variável python a informação do input nome do forms
        senha = request.form['senha'] #Adicionando a uma variável python a informação do input senha do forms
        session['nome'] = nome #Criando uma session para transportar essa informação de maneira segura entre as rotas
        return redirect(url_for('home'))
        '''
        ==========Possível validação usando arquivo .py do modelo==========
        if modelo.validação(nome, senha):
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
        '''

    else:
        return render_template('login.html')

@app.route('/Home')
def home():
    return render_template('home.html', nome = session['nome'])

if __name__ == '__main__':
    app.run(debug = True)