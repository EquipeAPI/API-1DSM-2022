from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)

# Configurações do banco de dados
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


def criaConta(nome, cpf, senha):
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO Cliente(cli_nome, cli_cpf, cli_senha) VALUES(%s, %s, %s)", (nome, cpf, senha)) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor

