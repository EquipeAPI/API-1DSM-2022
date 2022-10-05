from flask import Flask
from flask_mysqldb import MySQL
from app import mysql, app
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
    cur.execute("INSERT INTO usuario(nome_usuario, cpf_usuario, rua_avenida_usuario, numero_casa_usuario, bairro_usuario, cidade_usuario, estado_usuario, data_nascimento_usuario, genero_usuario, senha_usuario) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome'], forms ['CPF'], forms['rua'], forms['numero'], forms['bairro'], forms['cidade'], forms['estado'], forms['dataNascimento'], forms['genero'], forms['senha'])) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.execute(f"SELECT * FROM usuario WHERE nome_usuario =%s", [forms['nome']]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    id = cur.fetchone() 
    
    numero_agencia = modelo.atribuiAgencia()
    cur.execute("INSERT INTO conta(numero_conta, data_abertura_conta, id_usuario, numero_agencia) VALUES(%s, %s, %s, %s)", [numero_conta, dataAbertura, id['id_usuario'], numero_agencia]) #Criando linha na tabela conta
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None

def reqCriacao(forms):
    numero_agencia = modelo.atribuiAgencia()
    numero_conta = modelo.geradorNumeroConta() # Gera um número aleatório para atrelar à conta, esse número não será igual a mais nenhum outro do banco de dados
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO confirmacao_cadastro(nome_cadastro, cpf_cadastro, rua_avenida_cadastro, numero_casa_cadastro, bairro_cadastro, cidade_cadastro, estado_cadastro, data_nascimento_cadastro, genero_cadastro, senha_cadastro, numero_agencia, numero_conta) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome'], forms ['CPF'], forms['rua'], forms['numero'], forms['bairro'], forms['cidade'], forms['estado'], forms['dataNascimento'], forms['genero'], forms['senha'], numero_agencia, numero_conta)) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.close()
    return None


#Requisição de mudança de dados cadastrais
def reqMudanca(forms):
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute(f"INSERT INTO usuario(nome_usuario, cpf_usuario, rua_avenida_usuario, numero_usuario, bairro_usuario, cidade_usuario, estado_usuario, data_nascimento_usuario, genero_usuario, senha_usuario) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome'], forms ['cpf'], forms['rua'], forms['numero'], forms['bairro'], forms['cidade'], forms['estado'], forms['dataNascimento'], forms['genero'], forms['senha'])) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.close()
    return None


#insere linha de operação realisada ou requisitada (caso depósito) na tabela desejada.
def inserirOperacao(tabela, operacao, dic_dados): #id_usuário, operacao, valor, data e hora estão como um dicionário dicionário oq reduz esses parametros em um (será implementado na tarefa data e hora)
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO {tabela} (numero_conta, tipo_operacao, valor_operacao, data_hora, saldo_operacao) VALUES(%s, %s, %s, %s, %s)", (dic_dados['numero_conta'], operacao, dic_dados['valor'], dic_dados['dataHora'], dic_dados['saldoAntes']))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None

def reqDeposito(dic_dados): #id_usuário, operacao, valor, data e hora estão como um dicionário dicionário oq reduz esses parametros em um (será implementado na tarefa data e hora)
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO confirmacao_deposito (numero_conta, numero_agencia, valor_confirmacao_deposito, data_hora, saldo_operacao) VALUES(%s, %s, %s, %s, %s)", (dic_dados['numero_conta'], dic_dados['numero_agencia'], dic_dados['valor'], dic_dados['dataHora'], dic_dados['saldoAntes']))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None


#Requisicao de fechamento de conta
def reqFecha(id_usuário, numero_agencia, saldo):
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO (id_usuario) VALUES(%s, %s)", (id_usuário, tipo))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None