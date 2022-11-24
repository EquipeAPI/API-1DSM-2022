from asyncio.windows_events import NULL
from dataclasses import replace
from turtle import update
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

def entrouCheque(saldoAntes, id_usuario): #Diz se o usuário entrou ou não no cheque especial
    saldoAtual = bd.pegarDado('conta', 'id_usuario', id_usuario, 'saldo_conta')
    if saldoAntes>=0 and saldoAtual<0:
        bd.insereCheque(id_usuario)
        return None
    else:
        return None

def trataCPF(cpf): #tira os caracteres especiais do número de cpf
    cpf = cpf.replace('-', '')
    cpf = cpf.replace('.', '')
    return cpf

def validaOperacao(input):
    if '.' in input: # Verifica se há . no input dado pelo usuário
        controle = input.split('.') # Separa o . dos números
        if controle[0].isnumeric() and controle[1].isnumeric(): # confere se além do . havia somente números, que é o exigido
            if int(controle[0]) >= 0 and int(controle[1]) >=0:
                return True
            else:
                return False
        else:
            return False
    elif input.isnumeric() and int(input) >=0: # Caso não haja pontos confere se o usuário inseriu apenas números, caso contrário retorna falso
        return True
    else:
        return False

def validaData(data):
    dataAtual = bd.pegarDado('capital_banco', 'id_capital', 1, 'data_atual')
    data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
    if data >= dataAtual:
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

def mesmaContaGerente(numero_matricula, senha):
    linhaGerente = bd.pegarLinha('gerente_geral', 'numero_matricula', numero_matricula)
    linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', linhaGerente['id_usuario'])
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
    pagandoCheque(id_usuario, valor)
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
        pagandoCheque(id_recebedor, valor)
        return True
    else:
        return False

def dataHora(comHora): #Função que retor a data e a hora do sistema em string no formato AAAA/MM/DD - hor:min:seg
    dataHora = str(datetime.datetime.now()) #Pega a data e a hora do sistema em string
    dataHora = dataHora.replace('-', '/') #Troca os '-' por '/'
    dataHora = dataHora.replace(' ', ' - ') #Troca os '-' por '/'
    if comHora:
        dataHora = dataHora[0:21] #Tira os milissegundos
    else:
        dataHora = dataHora[0:10] #Tira as Horas
    return dataHora #Retorna a string já formatada devidamente

#Retorna a agencia a ser atribuida ao usuario que cadastrou, levando em conta qual agencia possui menos clientes

def atribuiAgencia():
    tabelaAgencia = bd.pegarTabela('agencia')
    agenciaUsuario = {}
    for linhaAgencia in tabelaAgencia:
        contador = 0
        agencia = linhaAgencia['numero_agencia']
        usuarios = bd.tabelaPersonalizada('conta', 'numero_agencia', agencia)
        requisicoes = bd.tabelaPersonalizada('confirmacao_cadastro', 'numero_agencia', agencia )
        for linhaUsuario in usuarios: #Contando quantos usuários tem na agencia em questão
            contador += 1
        for linhaUsuario in requisicoes:
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
    bd.apaga_linha('alteracao_cadastral', 'id_usuario', id_usuario)   
    #bd.apaga_linha('rendimento_poupanca', 'numero_conta', numero_conta)   
#   bd.apaga_linha('transacao','numero_conta_origem', numero_conta)
#   bd.apaga_linha('confirmacao_deposito', 'numero_conta', numero_conta)
    bd.apaga_linha('historico_operacao', 'numero_conta', numero_conta)
    bd.apaga_linha('conta', 'numero_conta', numero_conta)
#   bd.apaga_linha('agencia', 'id_usuario', id_usuario) 
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
        if valor == '' or valor == None or chave == 'id_alteracao' or chave == 'numero_agencia' or valor == '0' or chave == 'numero_matricula':
            continue
        else:
            cur.execute (f"update usuario set {chave} = '{valor}' where id_usuario = {id_usuario}")
    mysql.connection.commit() # Dando commit
    cur.close()
    return None

def dadosTransferenciaOrigem(operacoes):
    listaContasOrigem = []
    for operacao in operacoes:
        for coluna, registro in operacao.items():
            if coluna == 'numero_conta' and registro != None and registro != session['numero_conta']: #Se no histórico, o número da conta origem for diferente do número da conta logado == transferência foi recebida
                usuarioOrigem = bd.pegarLinha('conta', 'numero_conta', registro) 
                listaContasOrigem.append(usuarioOrigem) #Armazena as contas cujas transferências foram recebidas
    dadosUsuario = [] #listas vazias para iterar
    nomesOrigem = []
    dadosContas = []
    contasOrigem = []

    # ---- CONTAS DE TRANSFERÊNCIAS RECEBIDAS ----
    for conta in listaContasOrigem:
        for coluna, registro in conta.items():
            if coluna == 'id_usuario':
                dados = bd.pegarLinha('usuario', 'id_usuario', registro)
                cont = bd.pegarLinha('conta', 'id_usuario', registro )
                dadosUsuario.append(dados)
                dadosContas.append(cont)
    for usuario in dadosUsuario:
        nomesOrigem.append(usuario['nome_usuario'])

    for conta in dadosContas:
        contasOrigem.append(conta['numero_conta'])

    dic_nome_conta_origem = {}
    for nome in nomesOrigem:
        for conta in contasOrigem:
            dic_nome_conta_origem[nome] = conta
            contasOrigem.remove(conta)
            break

    return dic_nome_conta_origem

def dadosTransferenciaDestino(operacoes):
    listaContasDestino = []
    for operacao in operacoes:
        for coluna, registro in operacao.items():
            if coluna == 'numero_conta_destino' and registro != None and registro != session['numero_conta']: #Se no histórico, o número da conta destino for diferente do número da conta logado == transferência foi enviada pelo usuário
                usuarioDestino = bd.pegarLinha('conta', 'numero_conta', registro)
                listaContasDestino.append(usuarioDestino) #Armazena as contas cujas transferências foram enviadas
    dadosUsuario = [] #listas vazias para iterar
    nomesDestino = []
    dadosContas = []
    contasDestino = []

    # ---- CONTAS DE TRANSFERÊNCIAS ENVIADAS ----
    for conta in listaContasDestino:
        for coluna, registro in conta.items():
            if coluna == 'id_usuario':
                dados = bd.pegarLinha('usuario', 'id_usuario', registro)
                cont = bd.pegarLinha('conta', 'id_usuario', registro )
                dadosUsuario.append(dados)
                dadosContas.append(cont)
    for usuario in dadosUsuario:
        nomesDestino.append(usuario['nome_usuario'])

    for conta in dadosContas:
        contasDestino.append(conta['numero_conta'])

    dic_nome_conta_destino = {}
    for nome in nomesDestino:
        for conta in contasDestino:
            dic_nome_conta_destino[nome] = conta
            contasDestino.remove(conta)
            break

    return dic_nome_conta_destino



#=============================== FUNÇÕES DE CAPITAL TOTAL ===============================

def atualizaCapital():
    somaContas = bd.soma_capital('conta', 'saldo_conta')
    somaCheque = bd.soma_capital('conta', 'cheque_conta')
    somaContas = somaContas[0]['sum(saldo_conta)'] - somaCheque[0]['sum(cheque_conta)']
    inicial = bd.pegarTabela('capital_banco')
    inicial = inicial[0]['capital_inicial']
    #print(somaContas, inicial)
    atual = inicial + somaContas
    cur = mysql.connection.cursor()
    cur.execute (f"update capital_banco set capital_total = {atual} where id_capital = 1")
    mysql.connection.commit()
    cur.close()
    return None

#=============================== FUNÇÕES DE AGENCIA ===============================

def numeroAgenciaNull(valorAntigo, valor): # inserir 'Null' ou no valor, ou no valor antigo
    tabelaConta = bd.tabelaPersonalizada('conta', 'numero_agencia', valorAntigo)
    tabelaHistorico = bd.pegaHistoricoNumeroAgencia(valorAntigo)
    tabelaConfirmacaoCadastro = bd.tabelaPersonalizada('confirmacao_cadastro', 'numero_agencia', valorAntigo)
    tabelaAlteracaoCadastro = bd.tabelaPersonalizada('alteracao_cadastral', 'numero_agencia', valorAntigo)
    tabelaEncerraConta = bd.tabelaPersonalizada('encerramento_conta', 'numero_agencia', valorAntigo)
    listaTabelas = [tabelaConta, tabelaHistorico, tabelaConfirmacaoCadastro, tabelaAlteracaoCadastro, tabelaEncerraConta]
    if valor == 'Null':
        listaTexto = ['historico_operacao', 'confirmacao_cadastro', 'alteracao_cadastral', 'encerramento_conta', 'conta']
    elif valorAntigo == 'Null':
        listaTexto = ['conta', 'historico_operacao', 'confirmacao_cadastro', 'alteracao_cadastral', 'encerramento_conta']
    cur = mysql.connection.cursor()
    contador = 0
    if valorAntigo != 'Null':
        for tabela in listaTabelas:
            if listaTexto[contador] != 'historico_operacao':
                # return linha
                cur.execute (f"UPDATE {listaTexto[contador]} SET numero_agencia = {valor} WHERE numero_agencia = {valorAntigo}") 
            if listaTexto[contador]  == 'historico_operacao':
                cur.execute (f"UPDATE {listaTexto[contador]} SET numero_agencia_destino = {valor} WHERE numero_agencia_destino = {valorAntigo}")
                cur.execute (f"UPDATE {listaTexto[contador]} SET numero_agencia = {valor} WHERE numero_agencia = {valorAntigo}")
            mysql.connection.commit()
            contador += 1
    else:
        for tabela in listaTabelas:
            if listaTexto[contador] != 'historico_operacao':
                # return linha
                cur.execute (f"UPDATE {listaTexto[contador]} SET numero_agencia = {valor} WHERE numero_agencia is NULL")
            if listaTexto[contador]  == 'historico_operacao':
                cur.execute (f"UPDATE {listaTexto[contador]} SET numero_agencia_destino = {valor} WHERE numero_agencia_destino is NULL")  
                cur.execute (f"UPDATE {listaTexto[contador]} SET numero_agencia = {valor} WHERE numero_agencia is NULL")
            mysql.connection.commit()
            contador += 1
    cur.close()
    return None

def atualizaNumeroAgencia(dicionario, numero_antigo):
    tabelaAgencia = bd.pegarTabela('agencia')

    if not bd.valida('agencia', 'numero_agencia', dicionario['numero_agencia']):        
        if dicionario['numero_agencia'] != '':
            numeroAgenciaNull(numero_antigo, 'Null')
        bd.mudaAgencia(dicionario, numero_antigo) 
        if dicionario['numero_agencia'] != '':
            numeroAgenciaNull('Null', dicionario['numero_agencia'])
            
        return True
    else:
        return False

# Função para apagar agência
def apagaAgencia(valorAntigo, valor):
    dicionario = bd.pegarLinha('agencia', 'numero_agencia', valorAntigo)
    numeroAgenciaNull(valorAntigo, 'Null')
    if dicionario['numero_matricula'] != None:
        bd.atribuirDesatribuirGerente('desatribuir', dicionario['numero_matricula'], valorAntigo)
    numeroAgenciaNull('Null', valor)
    bd.apaga_linha('agencia', 'numero_agencia', valorAntigo)
    return None


def criacaoGerenteComAgencia(form, numero_agencia):
    id = bd.criacaoGerente(form, 'Sim')
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE agencia SET numero_matricula = {form['numero_matricula']} WHERE numero_agencia = {numero_agencia}")
    cur.execute(f"UPDATE conta SET numero_agencia = {numero_agencia} WHERE id_usuario = {id}")
    mysql.connection.commit()
    cur.close()
    return None

# Função para calcular rendimento de conta poupança
def rendimentoPoupança():
    saldo = bd.consultaSaldo(session['id_usuario'])
    jaRendeu = bd.pegarLinha('rendimento_poupanca', 'numero_conta', session['numero_conta'])

    if saldo > 0:
        operacao = bd.operacoesRendimento(session['numero_conta'])
        dataAtual = bd.diferencaDias()[0]

        if jaRendeu == None:
            dataInicial = operacao['data_hora_confirmacao']
        else:
            dataInicial = bd.pegarDado('rendimento_poupanca', 'numero_conta', session['numero_conta'], 'ultimo_rendimento')
            
        intervalo = (dataAtual - dataInicial).days
        rendimento = bd.pegarDado('capital_banco', 'id_capital', 1, 'taxa_rendimento')

        while intervalo >= 30:
            saldo = bd.consultaSaldo(session['id_usuario'])
            saldo_novo = saldo + (saldo * rendimento)
            valor = saldo_novo - saldo
            dataHora = dataInicial.date() + datetime.timedelta(days=30)
            dic_dados = {'numero_conta': session['numero_conta'], 'numero_agencia':session['numero_agencia'],'valor': valor, 'dataHora': dataHora, 'saldoAntes': saldo, 'operacao': 'Rendimento Poupança', 'status_operacao': 'Aprovado'} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
            bd.insereRendimento(session['numero_conta'], dataHora)
            bd.updateDado('conta', 'numero_conta', session['numero_conta'], 'saldo_conta', saldo_novo)
            bd.inserirOperacao('historico_operacao', 'Rendimento Poupança', dic_dados)
            
            intervalo = intervalo - 30

            dataInicial = bd.pegarDado('rendimento_poupanca', 'numero_conta', session['numero_conta'], 'ultimo_rendimento')

        return None
    else:
        if jaRendeu != None:
            bd.apaga_linha('rendimento_poupanca', 'numero_conta', session['numero_conta'])
            return saldo
        else:
            return saldo
    

#============================ FUNÇÕES DE TEMPO ===============================

def dataHora(comHora): #Função que retor a data e a hora do sistema em string no formato AAAA/MM/DD - hor:min:seg
    dataHora = str(datetime.datetime.now()) #Pega a data e a hora do sistema em string
    dataHora = dataHora.replace('-', '/') #Troca os '-' por '/'
    dataHora = dataHora.replace(' ', ' - ') #Troca os '-' por '/'
    if comHora:
        dataHora = dataHora[0:21] #Tira os milissegundos
    else:
        dataHora = dataHora[0:10] #Tira as Horas
    return dataHora #Retorna a string já formatada devidamente


#======================================== FUNÇÔES DE TRUNCAMENTO ========================================

def truncamentoSaldo(valor, id_usuario): #Trunca valor do saldo, a não ser que isso negative o capital total. Se esse for o caso, o valor em questão é arredondado
    valor = str(valor)
    capitalTotal = bd.pegarDado('capital_banco', 'id_capital', 1, 'capital_total')
    if float(valor) >= 0:
        resto = float(valor) - float(valor[:(valor.find('.')+3)])
        resultado = float(valor[:(valor.find('.')+3)])
        dicionario = {'resultado':resultado, 'resto':resto}
        truncamentoComBd(dicionario, id_usuario)
    else:
        resto = float(valor) - float(valor[:(valor.find('.')+3)])
        if capitalTotal + resto > 0.01:
            resultado = float(valor[:(valor.find('.')+3)])
            dicionario = {'resultado':resultado, 'resto':resto}
            truncamentoComBd(dicionario, id_usuario)
        else:
            valor = float(valor)
            valor = round(valor, 2)
            bd.mudaSaldo(valor, id_usuario)
            dicionario = {'reultado':valor}
    return dicionario
    

def truncaValor(valor):
    valor = str(valor)
    resto = float(valor) - float(valor[:(valor.find('.')+3)])
    capitalTotal = bd.pegarDado('capital_banco', 'id_capital', 1, 'capital_total')
    if float(valor) >= 0:
        resultado = float(valor[:(valor.find('.')+3)])
        dicionario = {'resultado':resultado, 'resto':resto}
        bd.somarValorCapital(dicionario['resto'])
    else:
        if capitalTotal + resto > 0.01: 
            resultado = float(valor[:(valor.find('.')+3)])
            dicionario = {'resultado':resultado, 'resto':resto}
            bd.somarValorCapital(dicionario['resto'])
        else:
            valor = float(valor)
            valor = round(valor, 2)
            #valor = str(valor)[:(valor.find('.')+3)]
            dicionario = {'resultado':valor}
    return dicionario['resultado']

def truncamentoComBd(dicionario, id_usuario):
    saque(id_usuario, dicionario['resto'])
    bd.somarValorCapital(dicionario['resto'])
    return None


#============================ FUNÇÂO DE CHEQUE ESPECIAL ============================

def pagandoCheque(id_usuario, valorEntrada):
    linhaConta = bd.pegarLinha('conta', 'id_usuario', id_usuario)
    if linhaConta['cheque_conta'] != 0:
        if abs(linhaConta['cheque_conta']) <= valorEntrada:
            bd.somarValorCapital(abs(linhaConta['cheque_conta']))
            bd.updateDividaCheque(id_usuario, 0)

            return None
        else:
            divida = linhaConta['cheque_conta'] + valorEntrada
            bd.somarValorCapital(valorEntrada)
            bd.updateDividaCheque(id_usuario, divida)
            return None
    else:
        return None

def aplicaJuros():
    juros = bd.pegarDado('capital_banco', 'id_capital', 1, 'taxa_juros')
    tabelaCheque = bd.pegarTabela('cheque_especial')
    dataAtual = bd.diferencaDias()[0]
    for linhaCheque in tabelaCheque:
        linhaConta = bd.pegarLinha('conta', 'numero_conta', linhaCheque['numero_conta'])
        dataUltimaAplicação = linhaCheque['data_cheque']
        while dataAtual - dataUltimaAplicação >= datetime.timedelta(days=1):
            linhaConta = bd.pegarLinha('conta', 'numero_conta', linhaCheque['numero_conta'])
            saldoAntigo = linhaConta['saldo_conta']
            desconto = saldoAntigo * juros
            desconto = truncaValor(desconto)
            saldoAtual = saldoAntigo + desconto
            valorDevendo = linhaConta['cheque_conta'] + desconto
            valorDevendo = truncaValor(valorDevendo) #truncando para evitar inconsistencias da limitante computacional de representação de números de ponto flutuante
            saldoAtual = truncaValor(saldoAtual) #truncando para evitar inconsistencias da limitante computacional de representação de números de ponto flutuante
            dataUltimaAplicação = dataUltimaAplicação + datetime.timedelta(1)
            bd.mudaSaldo(saldoAtual, linhaConta['id_usuario'])
            bd.updateCheque(linhaConta['id_usuario'], dataAtual, valorDevendo)
            dic_dados = {'dataHora':dataUltimaAplicação, 'data_hora_confirmacao':None, 'saldoAntes':saldoAntigo, 'valor':desconto, 'tipo_operacao':'Cheque Especial', 'numero_conta':linhaConta['numero_conta'], 'numero_agencia':linhaConta['numero_agencia'], 'status_operacao':'Aprovado', 'numero_conta_destino':None, 'numero_agencia_destino':None, 'saldo_operacao_destino':None}
            bd.inserirOperacao('historico_operacao', 'Cheque Especial', dic_dados)
    return None

def entrouCheque(saldoAntes, id_usuario): #Diz se o usuário entrou ou não no cheque especial
    saldoAtual = bd.pegarDado('conta', 'id_usuario', id_usuario, 'saldo_conta')
    if saldoAntes>=0 and saldoAtual<0:
        bd.insereCheque(id_usuario)
        return None
    else:
        return None

def saiuCheque(saldoAntes, id_usuario): #Diz se o usuário saiu ou não no cheque especial
    saldoAtual = bd.pegarDado('conta', 'id_usuario', id_usuario, 'saldo_conta')
    if saldoAntes<0 and saldoAtual>=0:
        bd.tiraCheque(id_usuario)
        return None
    else:
        return None
