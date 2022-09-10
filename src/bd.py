from flask import Flask
from flask_mysqldb import MySQL
from app import mysql

app = Flask(__name__)

# Configurações do banco de dados
''' app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Meusequel@d0'
app.config['MYSQL_DB'] = 'teste'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' '''


def criaConta(nome, cpf, senha):
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO Cliente(nome, cpf, senha) VALUES(%s, %s, %s)", (nome, cpf, senha)) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor

        
