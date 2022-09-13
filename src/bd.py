from flask import Flask
from flask_mysqldb import MySQL
from app import mysql

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'banco'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def criaConta(nome, cpf, rua, numero, bairro, cidade, estado, dataNascimento, genero, senha): #Insere uma linha com esses valores na tabela cliente
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO usuario(nome_usuario, cpf_usuario, rua_avenida_usuario, numero_usuario, bairro_usuario, cidade_usuario, estado_usuario, data_nascimento_usuario, genero_usuario, senha_usuario) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nome, cpf, rua, numero, bairro, cidade, estado, dataNascimento, genero, senha)) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    #cur.execute("INSERT INTO `conta`(`numero_conta`) VALUES()", [nome])
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor

        
def valida(tabela, dado, valor): #valida as informações
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela} WHERE {dado} =%s", [valor]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    usuario = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    if usuario != None:
        return True
    else:
        return False

def pegarLinha(tabela, coluna, valor): #retorna uma linha da coluna que possui o valor inserido
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela} WHERE {coluna} =%s", [valor]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    linha = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return linha

def consultaSaldo(nome):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT saldo FROM Conta WHERE nome =%s", [nome]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    saldo = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return saldo['saldo']

def mudaSaldo(valor, nome):
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE Conta SET saldo = {valor} WHERE nome = '{nome}'") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    saldo = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    mysql.connection.commit()
    cur.close()
    return None
    