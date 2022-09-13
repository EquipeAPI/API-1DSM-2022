from flask import Flask
from flask_mysqldb import MySQL
from app import mysql

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Goiabada2!'
app.config['MYSQL_DB'] = 'banco'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

def criaConta(forms): #Insere uma linha com esses valores na tabela cliente
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO usuario(nome_usuario, cpf_usuario, rua_avenida_usuario, numero_usuario, bairro_usuario, cidade_usuario, estado_usuario, data_nascimento_usuario, genero_usuario, senha_usuario) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome'], forms ['cpf'], forms['rua'], forms['numero'], forms['bairro'], forms['cidade'], forms['estado'], forms['dataNascimento'], forms['genero'], forms['senha'])) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.execute(f"SELECT id_usuario FROM usuario WHERE nome_usuario =%s", [forms['nome']]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    id = cur.fetchone() 
    cur.execute("INSERT INTO conta(id_usuario) VALUES(%s)", [id['id_usuario']]) #Criando linha na tabela conta
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

def consultaSaldo(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT saldo_conta FROM conta WHERE id_usuario ={id}") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    saldo = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return saldo['saldo_conta']

def mudaSaldo(valor, id):
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE conta SET saldo_conta = {valor} WHERE id_usuario = '{id}'") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    mysql.connection.commit()
    cur.close()
    return None
    