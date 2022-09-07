from flask import Flask, render_template, redirect 
from flask_mysqldb import MySQL

app = Flask(__name__)

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
    return render_template('index.html')

# Rota da página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota da página de login
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug = True)