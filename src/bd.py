from asyncio.windows_events import NULL
from flask import Flask
from flask_mysqldb import MySQL
from app import mysql
import modelo


        
def valida(tabela, dado, valor): #valida as informações
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela} WHERE {dado} =%s", [valor]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    usuario = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    if usuario != None:
        return True
    else:
        return False


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
    
#========================== Funções que pegam linhas ou tabelas no BD ==========================

def pegarLinha(tabela, coluna, valor): #retorna uma linha da coluna que possui o valor inserido
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela} WHERE {coluna} =%s", [valor]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    linha = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return linha

# Função que pega linhas 
def tabelaPersonalizada(tabela, dado, valor):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela} where {dado} = {valor}") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    tabelaPersonalizada = cur.fetchall() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return tabelaPersonalizada

def extratoPersonalizado(conta, data_inicio, data_fim):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM historico_operacao where numero_conta = %s AND data_hora_operacao >= %s AND data_hora_operacao <= %s", (conta, data_inicio, data_fim))
    extratoPersonalizado = cur.fetchall()
    cur.close()
    return extratoPersonalizado

# Função que pega uma tabela
def pegarTabela(tabela):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela}") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    tabelaSelecionada = cur.fetchall() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return tabelaSelecionada

#========================== Funções que inserem linhas no BD ==========================

def criaConta(forms, dataAbertura): #Insere uma linha com esses valores na tabela cliente
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO usuario(nome_usuario, cpf_usuario, rua_avenida_usuario, numero_casa_usuario, bairro_usuario, cidade_usuario, estado_usuario, data_nascimento_usuario, genero_usuario, senha_usuario) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome_cadastro'], forms ['cpf_cadastro'], forms['rua_avenida_cadastro'], forms['numero_casa_cadastro'], forms['bairro_cadastro'], forms['cidade_cadastro'], forms['estado_cadastro'], forms['data_naascimento_cadastro'], forms['genero_cadastro'], forms['senha_cadastro'])) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.execute(f"SELECT * FROM usuario WHERE nome_usuario =%s", [forms['nome_cadastro']]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    id = cur.fetchone() 
    numero_agencia = modelo.atribuiAgencia()
    cur.execute("INSERT INTO conta(numero_conta, data_abertura_conta, id_usuario, numero_agencia) VALUES(%s, %s, %s, %s)", [forms['numero_conta'], dataAbertura, id['id_usuario'], numero_agencia]) #Criando linha na tabela conta
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None

def reqCriacao(forms):
    numero_agencia = modelo.atribuiAgencia()
    numero_conta = modelo.geradorNumeroConta() # Gera um número aleatório para atrelar à conta, esse número não será igual a mais nenhum outro do banco de dados
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO confirmacao_cadastro(nome_cadastro, cpf_cadastro, rua_avenida_cadastro, numero_casa_cadastro, bairro_cadastro, cidade_cadastro, estado_cadastro, data_naascimento_cadastro, genero_cadastro, senha_cadastro, numero_agencia, numero_conta) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome'], forms ['CPF'], forms['rua'], forms['numero'], forms['bairro'], forms['cidade'], forms['estado'], forms['dataNascimento'], forms['genero'], forms['senha'], numero_agencia, numero_conta)) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.close()
    return None


#Requisição de mudança de dados cadastrais
def reqMudanca(dicionario, id_usuario, numero_agencia):
    forms = {}
    for chave, valor in dicionario.items():
        if dicionario[chave] == '':
            forms[chave] = None
        else:
            forms[chave] = valor
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute(f"INSERT INTO alteracao_cadastral(nome_alteracao, rua_avenida_alteracao, numero_casa_alteracao, bairro_alteracao, cidade_alteracao, estado_alteracao, genero_alteracao, id_usuario, numero_agencia, data_nascimento_alteracao) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome_usuario'], forms['rua_avenida_usuario'], forms['numero_casa_usuario'], forms['bairro_usuario'], forms['cidade_usuario'], forms['estado_usuario'], forms['genero_usuario'], id_usuario, numero_agencia, forms['data_nascimento_usuario'])) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.close()
    return None


#insere linha de operação realisada ou requisitada (caso depósito) na tabela desejada.
def inserirOperacao(tabela, operacao, dic_dados): #id_usuário, operacao, valor, data e hora estão como um dicionário dicionário oq reduz esses parametros em um (será implementado na tarefa data e hora)
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO {tabela} (numero_conta, numero_agencia, tipo_operacao, valor_operacao, data_hora_operacao, saldo_operacao, status_operacao) VALUES(%s, %s, %s, %s, %s, %s, %s)", (dic_dados['numero_conta'], dic_dados['numero_agencia'], operacao, dic_dados['valor'], dic_dados['dataHora'], dic_dados['saldoAntes'], dic_dados['status_operacao']))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None

""" def reqDeposito(dic_dados): #id_usuário, operacao, valor, data e hora estão como um dicionário dicionário oq reduz esses parametros em um (será implementado na tarefa data e hora)
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO confirmacao_deposito (numero_conta, numero_agencia, valor_confirmacao_deposito, data_hora, saldo_operacao) VALUES(%s, %s, %s, %s, %s, %s)", (dic_dados['numero_conta'], dic_dados['numero_agencia'], dic_dados['valor'], dic_dados['dataHora'], dic_dados['saldoAntes']))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None """

def atualizaDeposito(tabela, data_hora_confirmacao, status_novo, id):
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE {tabela} SET data_hora_confirmacao = %s, status_operacao = %s WHERE id_operacao = %s", (data_hora_confirmacao, status_novo, id))
    mysql.connection.commit() # Dando commit
    cur.close()
    return None

#Requisicao de fechamento de conta
def reqFecha(id_usuário, numero_agencia, saldo):
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO encerramento_conta(id_usuario, saldo_encerramento, numero_agencia) VALUES(%s, %s, %s)", (id_usuário, saldo, numero_agencia))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None


# ========================= Função de apagar linha ===========================

def apaga_linha(tabela, coluna, dado):
    cur = mysql.connection.cursor()
    cur.execute (f'delete from {tabela} where {coluna} = {dado} ')#Comendo DDL para apagar uma linha
    mysql.connection.commit()
    cur.close()
    return None


#================= Função para somar capital do banco ======================

def soma_capital(tabela, coluna):
    cur = mysql.connection.cursor()
    cur.execute (f'select sum({coluna}) from {tabela}')
    capital_total = cur.fetchall()
    cur.close()
    return capital_total






