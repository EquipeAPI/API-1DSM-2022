from flask import Flask, session
from flask_mysqldb import MySQL
import bd, random


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Goiabada2!'  #Insira aqui a senha do seu servidor local do MYSQL
app.config['MYSQL_DB'] = 'banco'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

def validaOperacao(input):
    if '.' in input: # Verifica se há . no input dado pelo usuário
        controle = input.split('.') # Separa o . dos números
        if len(controle) > 2: # Confere se havia apenas um . no input, que é o exigido
            return False
        elif controle[0].isnumeric() and controle[1].isnumeric() and len(controle[0]) <= 6: # confere se além do . havia somente números, que é o exigido
            return True
        else:
            return False
    elif input.isnumeric() and len(input) <= 6: # Caso não haja pontos confere se o usuário inseriu apenas números, caso contrário retorna falso
        return True
    else:
        return False


def geradorNumeroConta ():
    numero = random.sample(range(100000,1000000), 1) # Gera uma lista com um elemento numerico aleatório entre 100000 e 999999
    numero = numero[0] # retorna o inteiro que está na lista para a variável numero
    while bd.valida('conta', 'numero_conta', numero): # Confere se já há uma conta atrelada a esse número e repete o processo de geração até que o número gerado não esteja no banco de dados
        numero = random.sample(range(100000,1000000), 1)
        numero = numero[0]
    return numero # Retorna o número gerado

def mesmaConta(numero_conta, senha): #Confere se a senha e o numero da conta são referentes a mesma conta
    linhaConta = bd.pegarLinha('conta', 'numero_conta', numero_conta)
    id_usuario = linhaConta['id_usuario']
    linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', id_usuario)
    if linhaUsuario['senha_usuario'] == senha:
        return True
    else:
        return False

def saque(id_usuario, valor):
    valor = float(valor)
    atual = bd.pegarLinha('conta', 'id_usuario', id_usuario)
    atual = atual['saldo_conta'] - valor
    bd.mudaSaldo(atual, id_usuario)
    return None

def deposito(id_usuario, valor):
    valor = float(valor)
    atual = bd.pegarLinha('conta', 'id_usuario', id_usuario)
    atual = atual['saldo_conta'] + valor
    bd.mudaSaldo(atual, id_usuario)
    return None

def transferencia(id_usuario, valor, recebedor):
    if bd.valida('conta', 'numero_conta', recebedor):
        atualRecebedor = bd.pegarLinha('conta', 'numero_conta', recebedor)
        saque(id_usuario, valor)
        deposito(atualRecebedor['id_usuario'], valor)
        return True
    else:
        return False