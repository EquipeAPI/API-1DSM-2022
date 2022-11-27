from asyncio.windows_events import NULL
from turtle import mode
from flask import Flask
from flask_mysqldb import MySQL
from app import mysql
from datetime import datetime
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

def operacoesCorrecao(numero_conta):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM historico_operacao where numero_conta = {numero_conta} AND tipo_operacao = 'Correção Monetária' ORDER BY data_hora_operacao DESC")
    linha = cur.fetchone()
    cur.close()
    return linha

def pegarLinha(tabela, coluna, valor): #retorna uma linha da coluna que possui o valor inserido
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela} WHERE {coluna} =%s", [valor]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    linha = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return linha

def pegarDado(tabela, coluna, valor, dado): #retorna uma linha da coluna que possui o valor inserido
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela} WHERE {coluna} =%s", [valor]) #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    linha = cur.fetchone() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return linha[f'{dado}']

def tabelaPersonalizada(tabela, dado, valor):
    cur = mysql.connection.cursor()
    if isinstance(valor, str):
        cur.execute(f"SELECT * FROM {tabela} where {dado} = '{valor}'") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    else:
        cur.execute(f"SELECT * FROM {tabela} where {dado} = {valor}")
    tabelaPersonalizada = cur.fetchall() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return tabelaPersonalizada

def extrato(conta):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM historico_operacao WHERE numero_conta = {conta} or numero_conta_destino = {conta} ORDER BY data_hora_operacao DESC, saldo_operacao DESC") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    tabelaPersonalizada = cur.fetchall() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return tabelaPersonalizada

def extratoPersonalizado(conta, data_inicio, data_fim):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM historico_operacao WHERE (numero_conta = {conta} or numero_conta_destino = {conta}) AND data_hora_operacao BETWEEN %s and %s ORDER BY data_hora_operacao DESC", (data_inicio, data_fim))
    extratoPersonalizado = cur.fetchall()
    cur.close()
    return extratoPersonalizado

def operacoesRendimento(conta):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM historico_operacao WHERE (numero_conta = {conta} or numero_conta_destino = {conta}) AND (tipo_operacao = 'Depósito' OR tipo_operacao = 'Transferência') AND (status_operacao = 'Aprovado') AND (saldo_operacao = 0 or saldo_operacao_destino = 0) ORDER BY data_hora_confirmacao DESC LIMIT 1 ")
    operacoes = cur.fetchone()
    cur.close()
    return operacoes

def pegarTabela(tabela):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {tabela}") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    tabelaSelecionada = cur.fetchall() #Armazena todas as informações desse cliente na variável usuário
    cur.close()
    return tabelaSelecionada

#========================== Funções de cheque especial ==========================

def updateDividaCheque(id_usuario, valor):
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE conta SET cheque_conta = {valor} WHERE id_usuario = {id_usuario}")


def insereCheque(id_usuario): #Insere usuario na tabela de cheque especial
    numero_conta = pegarDado('conta', 'id_usuario', id_usuario, 'numero_conta')
    data = str(diferencaDias()[0])
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO cheque_especial(numero_conta, data_cheque) VALUES({numero_conta}, '{data}')")
    mysql.connection.commit()
    cur.close()
    return None

def tiraCheque(id_usuario):
    numero_conta = pegarDado('conta', 'id_usuario', id_usuario, 'numero_conta')
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM cheque_especial WHERE numero_conta = {numero_conta}")
    mysql.connection.commit()
    cur.close()
    return None

def updateCheque(id_usuario, novaData, valorCheque):
    numero_conta = pegarDado('conta', 'id_usuario', id_usuario, 'numero_conta')
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE conta SET cheque_conta = {valorCheque} WHERE numero_conta = {numero_conta}")
    cur.execute(f"UPDATE cheque_especial SET data_cheque = '{novaData}' WHERE numero_conta = {numero_conta}")
    mysql.connection.commit()
    cur.close()
    return None


#========================== Funções que inserem linhas no BD ==========================

def criaConta(forms, dataAbertura, req): #Insere uma linha com esses valores na tabela cliente
    dataHora = diferencaDias()[0]
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO usuario(nome_usuario, cpf_usuario, rua_avenida_usuario, numero_casa_usuario, bairro_usuario, cidade_usuario, estado_usuario, data_nascimento_usuario, genero_usuario, senha_usuario, data_hora_usuario) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome_cadastro'], forms ['cpf_cadastro'], forms['rua_avenida_cadastro'], forms['numero_casa_cadastro'], forms['bairro_cadastro'], forms['cidade_cadastro'], forms['estado_cadastro'], forms['data_naascimento_cadastro'], forms['genero_cadastro'], forms['senha_cadastro'], diferencaDias()[0])) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit() # Dando commit
    cur.execute(f"SELECT * FROM usuario WHERE data_hora_usuario ='{dataHora}'") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    id = cur.fetchone() 
    if req:
        cur.execute("INSERT INTO conta(numero_conta, data_abertura_conta, id_usuario, numero_agencia, tipo_conta) VALUES(%s, %s, %s, %s, %s)", (forms['numero_conta'], dataAbertura, id['id_usuario'], forms['numero_agencia'], forms['tipo_cadastro'])) #Criando linha na tabela conta
    else:
        numero_agencia = modelo.atribuiAgencia()
        cur.execute("INSERT INTO conta(numero_conta, data_abertura_conta, id_usuario, numero_agencia, tipo_conta) VALUES(%s, %s, %s, %s, %s)", (forms['numero_conta'], dataAbertura, id['id_usuario'], numero_agencia, forms['tipo_cadastro'])) #Criando linha na tabela conta
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None

def reqCriacao(forms):
    numero_agencia = modelo.atribuiAgencia()
    numero_conta = modelo.geradorNumeroConta() # Gera um número aleatório para atrelar à conta, esse número não será igual a mais nenhum outro do banco de dados
    cur = mysql.connection.cursor() #Abrindo um cursor pra navegar no SQL
    cur.execute("INSERT INTO confirmacao_cadastro(nome_cadastro, cpf_cadastro, rua_avenida_cadastro, numero_casa_cadastro, bairro_cadastro, cidade_cadastro, estado_cadastro, data_naascimento_cadastro, genero_cadastro, senha_cadastro, numero_agencia, numero_conta, tipo_cadastro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forms['nome'], forms ['CPF'], forms['rua'], forms['numero'], forms['bairro'], forms['cidade'], forms['estado'], forms['dataNascimento'], forms['genero'], forms['senha'], numero_agencia, numero_conta, forms['tipo_conta'])) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
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

def configuracaoInicial(form):
    if '%' in str(form['taxa_juros']):
        taxa_juros = form['taxa_juros']
        taxa_juros = taxa_juros.rstrip(taxa_juros[-1])
        if ',' in taxa_juros:
            taxa_juros = taxa_juros.replace(',', '.')
        taxa_juros = float(taxa_juros)/100
    else:
        taxa_juros = form['taxa_juros']
    
    if '%' in str(form['taxa_rendimento']):
        taxa_rendimento = form['taxa_rendimento']
        taxa_rendimento = taxa_rendimento.rstrip(taxa_rendimento[-1])
        if ',' in taxa_rendimento:
            taxa_rendimento = taxa_rendimento.replace(',','.')
        taxa_rendimento = float(taxa_rendimento)/100
    else:
        taxa_rendimento = form['taxa_rendimento']

    if '%' in str(form['correcao_monetaria']):
        correcao_monetaria = form['correcao_monetaria']
        correcao_monetaria = correcao_monetaria.rstrip(correcao_monetaria[-1])
        if ',' in correcao_monetaria:
            correcao_monetaria = correcao_monetaria.replace(',','.')
        correcao_monetaria = float(correcao_monetaria)/100
    else:
        taxa_rendimento = form['taxa_rendimento']
    
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE capital_banco SET capital_inicial = %s, capital_total = %s, data_atual = %s, taxa_juros = %s, taxa_rendimento = %s, correcao_monetaria = %s WHERE id_capital = 1", (form['capital_inicial'], form['capital_inicial'], form['data_atual'], taxa_juros, taxa_rendimento, correcao_monetaria))
    mysql.connection.commit()
    cur.close()
    return None

def configuracoesSeguintes(form):
    if '%' in str(form['taxa_juros']):
        taxa_juros = form['taxa_juros']
        taxa_juros = taxa_juros.rstrip(taxa_juros[-1])
        if ',' in taxa_juros:
            taxa_juros = taxa_juros.replace(',', '.')
        taxa_juros = float(taxa_juros)/100
    else:
        taxa_juros = form['taxa_juros']
    
    if '%' in str(form['taxa_rendimento']):
        taxa_rendimento = form['taxa_rendimento']
        taxa_rendimento = taxa_rendimento.rstrip(taxa_rendimento[-1])
        if ',' in taxa_rendimento:
            taxa_rendimento = taxa_rendimento.replace(',','.')
        taxa_rendimento = float(taxa_rendimento)/100
    else:
        taxa_rendimento = form['taxa_rendimento']
        
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE capital_banco SET data_atual = %s, taxa_juros = %s, taxa_rendimento = %s WHERE id_capital = 1", (form['data_atual'], taxa_juros, taxa_rendimento))
    mysql.connection.commit()
    cur.close()
    return None

def diferencaDias():
    cur = mysql.connection.cursor()
    data = str(pegarDado('capital_banco', 'id_capital', 1, 'data_atual'))
    cur.execute(f" SELECT datediff('{data}', now()) as intervalo")
    intervalo = cur.fetchone()['intervalo']
    cur.execute(f" SELECT now() + INTERVAL {intervalo} day as data")
    data = cur.fetchone()['data']
    return data, intervalo

def insereRendimento(conta, data):
    cur = mysql.connection.cursor()
    cur.execute(f" INSERT INTO rendimento_poupanca(numero_conta, ultimo_rendimento) VALUES({conta}, '{data}') ON DUPLICATE KEY UPDATE ultimo_rendimento = '{data}'")
    mysql.connection.commit()
    cur.close()
    return None

def somarValorCapital(valor):
    cur =mysql.connection.cursor()
    cur.execute("select capital_inicial from capital_banco")
    capital = cur.fetchone()
    capitalAtualizado = float(capital['capital_inicial']) + float(valor)
    cur.execute(f"update capital_banco set capital_inicial = {capitalAtualizado} where capital_inicial = {capital['capital_inicial']}")
    cur.connection.commit()
    cur.close()
    return None

#insere linha de operação realizada ou requisitada (caso depósito) na tabela desejada.
def inserirOperacao(tabela, operacao, dic_dados): #id_usuário, operacao, valor, data e hora estão como um dicionário dicionário oq reduz esses parametros em um (será implementado na tarefa data e hora)
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO {tabela} (numero_conta, numero_agencia, tipo_operacao, valor_operacao, data_hora_operacao, saldo_operacao, status_operacao) VALUES(%s, %s, %s, %s, %s, %s, %s)", (dic_dados['numero_conta'], dic_dados['numero_agencia'], operacao, dic_dados['valor'], dic_dados['dataHora'], dic_dados['saldoAntes'], dic_dados['status_operacao']))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None

def inserirOperacaoTransferencia(tabela, operacao, dic_dados): #id_usuário, operacao, valor, data e hora estão como um dicionário dicionário oq reduz esses parametros em um (será implementado na tarefa data e hora)
    cur = mysql.connection.cursor()
    cur.execute (f"INSERT INTO {tabela} (numero_conta, numero_agencia, tipo_operacao, valor_operacao, data_hora_operacao, data_hora_confirmacao, saldo_operacao, status_operacao, numero_conta_destino, numero_agencia_destino, saldo_operacao_destino) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (dic_dados['numero_conta'], dic_dados['numero_agencia'], operacao, dic_dados['valor'], dic_dados['dataHora'], dic_dados['dataHora'], dic_dados['saldoAntes'], dic_dados['status_operacao'], dic_dados['contaDestino'], dic_dados['numero_agencia_recebedor'], dic_dados['saldoAntesRecebedor']))
    mysql.connection.commit() # Dando commit
    cur.close() # Fechando o cursor
    return None

def atualizaDeposito(tabela, data_hora_confirmacao, status_novo, id):
    tabelaHistorico = tabelaPersonalizada('historico_operacao', 'status_operacao', "'Pendente'")
    cur = mysql.connection.cursor()
    if id != 0:
        cur.execute(f"UPDATE {tabela} SET data_hora_confirmacao = %s, status_operacao = %s WHERE id_operacao = %s", (data_hora_confirmacao, status_novo, id))
    else:
        contador = 0
        for linha in tabelaHistorico:
            if contador == 0:
                id = linha['id_operacao']
                contador += 1
            else:
                if id >= linha['id_operacao']:
                    continue
                else:
                    id = linha['id_operacao']
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

# ========================= Função de UPDATE de um dado ===========================

def updateDado(tabela, whereColuna, whereDado, coluna, dado):
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE {tabela} SET {coluna} = {dado} WHERE {whereColuna} = {whereDado}")
    mysql.connect.commit()
    cur.close()
    return None

# ========================= Função de apagar linha ===========================

def apaga_linha(tabela, coluna, dado):
    cur = mysql.connection.cursor()
    cur.execute (f'delete from {tabela} where {coluna} = {dado} ')#Comando DDL para apagar uma linha
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

#================= Funções de agencia ======================

def mudaAgencia(dicionario, numero_antigo):
    cur = mysql.connection.cursor()
    for chave, valor in dicionario.items():
        if dicionario[chave] == '':
            continue
        else:
            cur.execute (f"UPDATE agencia SET {chave} = '{valor}' WHERE numero_agencia = {numero_antigo}")
    mysql.connection.commit()
    cur.close()
    return None

def mudaMatricula(numero_matricula, numero_antigo):
    cur = mysql.connection.cursor()
    cur.execute(f'UPDATE agencia SET numero_matricula = NULL WHERE numero_matricula = {numero_antigo}')
    cur.execute(f'UPDATE gerente_geral SET numero_matricula = {numero_matricula} WHERE numero_matricula = {numero_antigo}')
    cur.execute(f'UPDATE agencia SET numero_matricula = {numero_matricula} WHERE numero_matricula is NULL')
    mysql.connection.commit()
    cur.close()
    return None

def criacaoAgencia(form, atribuido):
    cur = mysql.connection.cursor()
    if atribuido:
        cur.execute(f"INSERT INTO agencia (numero_agencia, numero_matricula, nome_agencia, rua_avenida_agencia, numero_local_agencia, bairro_agencia, cidade_agencia, estado_agencia) VALUES ('{form['numero_agencia']}', {form['numero_matricula']}, '{form['nome_agencia']}', '{form['rua_avenida_agencia']}', '{form['numero_local_agencia']}', '{form['bairro_agencia']}', '{form['cidade_agencia']}', '{form['estado_agencia']}' )")
        cur.execute(f"UPDATE gerente_geral SET atribuicao = 'SIM' WHERE numero_matricula = {form['numero_matricula']}")
    else:
        cur.execute(f"INSERT INTO agencia (numero_agencia, nome_agencia, rua_avenida_agencia, numero_local_agencia, bairro_agencia, cidade_agencia, estado_agencia) VALUES ({form['numero_agencia']}, '{form['nome_agencia']}', '{form['rua_avenida_agencia']}', '{form['numero_local_agencia']}', '{form['bairro_agencia']}', '{form['cidade_agencia']}', '{form['estado_agencia']}')")
    mysql.connection.commit()
    cur.close()
    return None

def criacaoGerente(form, atribuicao):
    numero_conta = modelo.geradorNumeroConta()
    dataHora = diferencaDias()[0]
    dataAbertura = str(dataHora)[0:10]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuario(nome_usuario, cpf_usuario, rua_avenida_usuario, numero_casa_usuario, bairro_usuario, cidade_usuario, estado_usuario, data_nascimento_usuario, genero_usuario, senha_usuario, data_hora_usuario) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (form['nome_usuario'], form ['CPF'], form['rua'], form['numero'], form['bairro'], form['cidade'], form['estado'], form['dataNascimento'], form['genero'], form['senha'], dataHora)) # Executando o comando de inserir os dados na tabela. "%s" representa uma variável que eu defini nos parenteses seguintes
    mysql.connection.commit()
    cur.execute(f"SELECT * FROM usuario WHERE data_hora_usuario ='{dataHora}'") #Procura pelo cliente cujo CPF bata com o que foi digitado no formulário de login
    id = cur.fetchone() 
    cur.execute("INSERT INTO conta(numero_conta, data_abertura_conta, id_usuario, numero_agencia, tipo_conta) VALUES(%s, %s, %s, %s, %s)", (numero_conta, dataAbertura, id['id_usuario'], None, 'Corrente')) #Criando linha na tabela conta
    cur.execute(f"INSERT INTO gerente_geral(id_usuario, numero_matricula, tipo_gerente, atribuicao) VALUES({id['id_usuario']}, {form['numero_matricula']}, 'Gerente de Agência', '{atribuicao}')")
    mysql.connection.commit()
    cur.close()
    id = id['id_usuario']
    return id


#===================================== Atribui/Desatribui agência =====================================
def pegaHistoricoNumeroConta(numero_conta):
    cur = mysql.connection.cursor()
    cur.execute(f'Select * FROM historico_operacao WHERE numero_conta = {numero_conta} or numero_conta_destino = {numero_conta}')
    tabela = cur.fetchall()
    cur.close()
    return tabela

def pegaHistoricoNumeroAgencia(numero_agencia):
    cur = mysql.connection.cursor()
    cur.execute(f'Select * FROM historico_operacao WHERE numero_conta = {numero_agencia} or numero_conta_destino = {numero_agencia}')
    tabela = cur.fetchall()
    cur.close()
    return tabela


def atribuirDesatribuirGerente(acao, numero_matricula, numero_agencia):
    linhaGerente = pegarLinha('gerente_geral', 'numero_matricula', numero_matricula)
    linhaConta = pegarLinha('conta', 'id_usuario', linhaGerente['id_usuario'])
    tabelaHistorico = pegaHistoricoNumeroConta(linhaConta['numero_conta'])
    tabelaAlteracaoCadastro = tabelaPersonalizada('alteracao_cadastral', 'id_usuario', linhaGerente['id_usuario'])
    tabelaEncerraConta = tabelaPersonalizada('encerramento_conta', 'id_usuario', linhaGerente['id_usuario'])
    
    cur = mysql.connection.cursor()
    
    if acao == 'desatribuir':
        cur.execute(f"UPDATE agencia SET numero_matricula = NULL WHERE numero_matricula = {numero_matricula}")
        cur.execute(f"UPDATE gerente_geral SET atribuicao = 'Nao' WHERE numero_matricula = {numero_matricula}")
        if numero_agencia != 0:
            cur.execute(f"UPDATE historico_operacao SET numero_agencia = NULL WHERE numero_agencia = {linhaConta['numero_agencia']}")
        '''for linha in tabelaAlteracaoCadastro:
            cur.execute(f"UPDATE ateracao_cadastral SET numero_agencia = NULL WHERE id_usuario = {linhaGerente['id_usuario']}")
        for linha in tabelaEncerraConta:
            cur.execute(f"UPDATE encerramento_conta SET numero_agencia = NULL WHERE id_usuario = {linhaGerente['id_usuario']}")'''
        cur.execute(f"UPDATE conta SET numero_agencia = NULL WHERE id_usuario ={linhaGerente['id_usuario']}")
        if numero_agencia != 0:
            cur.execute(f"UPDATE historico_operacao SET numero_agencia = {numero_agencia} WHERE numero_agencia is NULL")
        
    else:
        cur.execute(f"UPDATE agencia SET numero_matricula = {numero_matricula} WHERE numero_agencia = {numero_agencia}")
        cur.execute(f"UPDATE gerente_geral SET atribuicao = 'Sim' WHERE numero_matricula = {numero_matricula}")
        '''for linha in tabelaHistorico:
            cur.execute(f"UPDATE historico_operacao SET numero_agencia = {numero_agencia} WHERE numero_conta = {linhaConta['numero_conta']}")
        for linha in tabelaAlteracaoCadastro:
            cur.execute(f"UPDATE ateracao_cadastral SET numero_agencia = {numero_agencia} WHERE id_usuario = {linhaGerente['id_usuario']}")
        for linha in tabelaEncerraConta:
            cur.execute(f"UPDATE encerramento_conta SET numero_agencia = {numero_agencia} WHERE id_usuario = {linhaGerente['id_usuario']}")'''
        cur.execute(f"UPDATE conta SET numero_agencia = {numero_agencia} WHERE id_usuario ={linhaGerente['id_usuario']}")
    mysql.connection.commit()
    cur.close()
    return None

#