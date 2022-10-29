from dataclasses import replace
from flask import Flask, session
from flask_mysqldb import MySQL
import bd, random
import datetime


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Goiabada2!'  #Insira aqui a senha do seu servidor local do MYSQL
app.config['MYSQL_DB'] = 'banco'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)


def trataCPF(cpf): #tira os caracteres especiais do número de cpf
    cpf = cpf.replace('-', '')
    cpf = cpf.replace('.', '')
    return cpf

def validaOperacao(input):
    if '.' in input: # Verifica se há . no input dado pelo usuário
        controle = input.split('.') # Separa o . dos números
        if controle[0].isnumeric() and controle[1].isnumeric(): # confere se além do . havia somente números, que é o exigido
            return True
        else:
            return False
    elif input.isnumeric(): # Caso não haja pontos confere se o usuário inseriu apenas números, caso contrário retorna falso
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
        atualEnvio = bd.pegarLinha('conta', 'id_usuario', id_usuario)
        id_recebedor = atualRecebedor['id_usuario']
        valor = float(valor)
        atualEnvio = atualEnvio['saldo_conta'] - valor
        atualRecebedor = atualRecebedor['saldo_conta'] + valor
        bd.mudaSaldo(atualEnvio, id_usuario)
        bd.mudaSaldo(atualRecebedor, id_recebedor)
        return True
    else:
        return False

def dataHora(comHora): #Função que retor a data e a hora do sistema em string no formato AAAA/MM/DD - hor:min:seg
    dataHora = str(datetime.datetime.now()) #Pega a data e a hora do sistema em string
    dataHora = dataHora.replace('-', '/') #Troca os '-' por '/'
    dataHora = dataHora.replace(' ', ' - ') #Troca os '-' por '/'
    if comHora:
        dataHora = dataHora[0:19] #Tira os milissegundos
    else:
        dataHora = dataHora[0:10] #Tira as Horas
    return dataHora #Retorna a string já formatada devidamente

#Retorna a agencia a ser atribuida ao usuario que cadastrou, levando em conta qual agencia possui menos clientes

def atribuiAgencia():
    tabelaAgencia = bd.pegarTabela('gerente_agencia')
    agenciaUsuario = {}
    for linhaAgencia in tabelaAgencia:
        contador = 0
        agencia = linhaAgencia['numero_agencia']
        usuarios = bd.tabelaPersonalizada('conta', 'numero_agencia', agencia)
        for linhaUsuario in usuarios: #Contando quantos usuários tem na agencia em questão
            contador += 1
        agenciaUsuario[f'{agencia}'] = contador  #Dicionário que relaciona a agencia com o número de usuários cadastrados nela

    for chave, valor in agenciaUsuario.items(): #Seleciona a agencia que possui menos usuarios
        if int(chave) == 1:
            chaveMenor = chave
            valorMenor = valor
        elif valor < valorMenor:
            chaveMenor = chave
            valorMenor = valor
        else:
            continue
    return chaveMenor #retorna a agencia que tem menos usuario

# Função para apagar usuário do banco
def apagaUsuario(numero_conta, id_usuario):
    bd.apaga_linha('encerramento_conta', 'id_usuario', id_usuario)       
    bd.apaga_linha('transacao','numero_conta_origem', numero_conta)
    bd.apaga_linha('confirmacao_deposito', 'numero_conta', numero_conta)
    bd.apaga_linha('historico_operacao', 'numero_conta', numero_conta)
    bd.apaga_linha('conta', 'numero_conta', numero_conta)
    bd.apaga_linha('gerente_agencia', 'id_usuario', id_usuario)
    bd.apaga_linha('alteracao_cadastral', 'id_usuario', id_usuario) 
    bd.apaga_linha('usuario', 'id_usuario', id_usuario)
    return None 

#função para alterar cadastro apartir de uma requisição
def alteraPorRequisicao(id_usuario):
    cur = mysql.connection.cursor()
    dicionario = bd.pegarLinha('alteracao_cadastral', 'id_usuario', id_usuario)
    for chave, valor in dicionario.items():
        if valor == '' or valor == None or chave == 'id_alteracao' or chave == 'numero_agencia' or valor == '0':
            continue
        else:
            chave = chave.replace('alteracao', 'usuario')
            cur.execute (f"update usuario set {chave} = '{valor}' where id_usuario = {id_usuario}")
    mysql.connection.commit() # Dando commit
    cur.close()
    return None

def alteraPorGerente(linhaAlteracao, id_usuario):
    cur = mysql.connection.cursor()
    for chave, valor in linhaAlteracao.items():
        if valor == '' or valor == None or chave == 'id_alteracao' or chave == 'numero_agencia' or valor == '0':
            continue
        else:
            cur.execute (f"update usuario set {chave} = '{valor}' where id_usuario = {id_usuario}")
    mysql.connection.commit() # Dando commit
    cur.close()
    return None


#=============================== FUNÇÕES DE CAPITAL TOTAL ===============================

def atualizaCapital():
    somaContas = bd.soma_capital('conta', 'saldo_conta')
    somaContas = somaContas[0]['sum(saldo_conta)']
    inicial = bd.pegarTabela('capital_banco')
    inicial = inicial[0]['capital_inicial']
    atual = int(inicial) + somaContas
    cur = mysql.connection.cursor()
    cur.execute (f"update capital_banco set capital_total = {atual} where id_capital = 0")
    mysql.connection.commit()
    return None


