
from urllib import response
from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from flask_mysqldb import MySQL

import bd, modelo # Importando os outros arquivos .py

app = Flask(__name__)
app.secret_key = 'aonainfinnBFNFOANOnasfononfsa' #Chave de segurança da session

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Goiabada2!' #Insira aqui a senha do seu servidor local do MYSQL
app.config['MYSQL_DB'] = 'banco'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# Rota da página de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        dadosCliente = request.form # Armazena todos os dados inseridos no formulário em uma variável tipo dicionário
        if dadosCliente['senha'] == dadosCliente['senhaConfirma']:
            bd.reqCriacao(dadosCliente) #Insere os valores do formulário na tabela cliente
            linhaReq = bd.pegarLinha('confirmacao_cadastro', 'cpf_cadastro', dadosCliente['CPF']) # Pegando a linha da tabela confirmacao_cadastro para acessar o numero da conta na linha seguinte
            numero_conta = linhaReq['numero_conta'] # Guardando numero_usuario para ser usado em outras telas
            flash(f'Requisição de abertura de conta enviada para o gerente.' ) # Mensagem que informa qual o número do usuário
            flash(f'O seu número de conta será: {numero_conta}.')
            flash(f'Ele será necessário para acessar sua conta.')
                
            return redirect(url_for('login'))
        else:
            flash('Senha e confimação de senha devem ser iguais.')
            return render_template('cadastro.html')
    else:
        return render_template('cadastro.html')



#======================================= LOGINS =======================================

# Rota da página de login (que é a página inicial)
@app.route('/', methods=['POST', 'GET']) # As duas rotas acionaram a mesma função
@app.route('/login', methods=['POST', 'GET']) # Colocando os metodos HTTP que serão usados
def login():
    #if 'nome' in session: #Verificando se a pessoa já está logada
        #return redirect(url_for('home'))
    if request.method == 'POST': #Se a pessoa apertar o botão 'ENTRAR' do forms
        numero_conta = request.form['numero_conta'] #Adicionando a uma variável python a informação do input cpf do forms
        senha = request.form['senha'] #Adicionando a uma variável python a informação do input senha do forms
        
        if bd.valida("conta", "numero_conta", numero_conta) and bd.valida("usuario", "senha_usuario", senha) and modelo.mesmaConta(numero_conta, senha): #Inserir tabela, coluna, valor para ver se o valor existe na coluna da tabela, se existir retorna True. Se corretas confere se são referentes a mesma conta (modelo.mesmaConta)
            linhaConta = bd.pegarLinha('conta', 'numero_conta', numero_conta) #Função que retorna os valores da linha da tabela escolhida (tabela, coluna, valor da linha requisitada)
            linhaUsuario = bd.pegarLinha("usuario", "id_usuario", linhaConta['id_usuario'])
            if not bd.valida('gerente_geral', 'id_usuario', linhaUsuario['id_usuario']):
                session['nome'] = linhaUsuario['nome_usuario'] # Guardando nome_usuario para ser usado em outras telas
                session['id_usuario'] = linhaUsuario['id_usuario'] # Guardando id_usuario para ser usado em outras telas
                session['numero_conta'] = linhaConta['numero_conta'] # Guardando numero_usuario para ser usado em outras telas
                session['numero_agencia'] = linhaConta['numero_agencia']
                session['gerente'] = 'nao'
                return redirect(url_for('home'))
            else:
                flash("Número inserido é um número de gerente", "info")
                return redirect(url_for('loginGerente'))
            
        else:
            flash("Número da Conta ou Senha incorretos", "info")
            return redirect(url_for('login'))
        
    else:
        return render_template('login.html')

#LOGIN GERENTE
@app.route('/loginGerente', methods = ['POST', 'GET'])
def loginGerente():
    if request.method == 'POST': #Se a pessoa apertar o botão 'ENTRAR' do forms
        numero_conta = request.form['numero_conta'] #Adicionando a uma variável python a informação do input cpf do forms
        senha = request.form['senha'] #Adicionando a uma variável python a informação do input senha do forms
        
        if bd.valida("conta", "numero_conta", numero_conta) and bd.valida("usuario", "senha_usuario", senha) and modelo.mesmaConta(numero_conta, senha): #Inserir tabela, coluna, valor para ver se o valor existe na coluna da tabela, se existir retorna True. Se corretas confere se são referentes a mesma conta (modelo.mesmaConta)
            linhaConta = bd.pegarLinha('conta', 'numero_conta', numero_conta) #Função que retorna os valores da linha da tabela escolhida (tabela, coluna, valor da linha requisitada)
            linhaUsuario = bd.pegarLinha("usuario", "id_usuario", linhaConta['id_usuario'])
            if bd.valida('gerente_geral', 'id_usuario', linhaUsuario['id_usuario']):
                session['nome'] = linhaUsuario['nome_usuario'] # Guardando nome_usuario para ser usado em outras telas
                session['id_usuario'] = linhaUsuario['id_usuario'] # Guardando id_usuario para ser usado em outras telas
                session['numero_conta'] = linhaConta['numero_conta'] # Guardando numero_usuario para ser usado em outras telas
                session['numero_agencia'] = linhaConta['numero_agencia']
                linhaGerente = bd.pegarLinha('gerente_geral', 'id_usuario', session['id_usuario'])
                if linhaGerente['tipo_gerente'] == 'Gerente Geral':
                    session['gerente'] = 'geral'
                    return redirect(url_for('homeGerenteGeral'))
                else:
                    session['gerente'] = 'agencia'
                    return redirect(url_for('homeGerenteAgencia'))
            else:
                flash("Esse não é o número de um gerente. Você foi redirecionado para o login de usuário normal", "info")
                return redirect(url_for('login'))
        else:
            flash("Número da Conta ou Senha incorretos", "info")
            return redirect(url_for('loginGerente'))
        
    else:
        return render_template('login.html', gerente = 'SIM')




#======================================= ROTAS HOME =======================================

# Rota da página home
@app.route('/home')
def home():
    modelo.atualizaCapital()
    if 'nome' in session:
        if 'dic_dados' in session: #Se há algum dado de operação na session, ele será apagado.
            session.pop('dic_dados', None)
        return render_template('home.html', nome = session['nome'],
        saldo = bd.consultaSaldo(session['id_usuario']),
        numero_conta = str(session['numero_conta']),
        numero_agencia = str(session['numero_agencia']), gerente = session['gerente'])
    else:
        return redirect(url_for('login'))

@app.route('/homeGerenteAgencia')
def homeGerenteAgencia():
    modelo.atualizaCapital()
    if session['gerente'] == 'agencia':
        if 'dic_dados' in session: #Se há algum dado de operação na session, ele será apagado.
            session.pop('dic_dados', None)
        linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', session['id_usuario'])
        session['nome'] = linhaUsuario['nome_usuario']
        return render_template('homegerente.html', nome = session['nome'],
        saldo = bd.consultaSaldo(session['id_usuario']),
        numero_conta = str(session['numero_conta']),
        numero_agencia = str(session['numero_agencia']), gerente = session['gerente'])
    else:
        return redirect(url_for('login'))


@app.route('/homeGerenteGeral')
def homeGerenteGeral():
    modelo.atualizaCapital()
    if session['gerente'] == 'geral':
        if 'dic_dados' in session: #Se há algum dado de operação na session, ele será apagado.
            session.pop('dic_dados', None)
        linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', session['id_usuario'])
        session['nome'] = linhaUsuario['nome_usuario']
        capitalTotal = bd.pegarLinha('capital_banco', 'id_capital', 0)
        capitalTotal = capitalTotal['capital_total']
        return render_template('homegerentegeral.html', nome = session['nome'],
        saldo = bd.consultaSaldo(session['id_usuario']),
        numero_conta = str(session['numero_conta']),
        numero_agencia = str(session['numero_agencia']), gerente = session['gerente'], capitalTotal = capitalTotal)
    else:
        return redirect(url_for('login'))




#======================================= OPERAÇÕES =======================================



@app.route('/deposito', methods = ['POST', 'GET'])
def deposito():
    if 'nome' in session: # Se o usuário não está logado, retorna para a tela de login, caso contrário reenderiza a tela de depósito
        if request.method == 'POST':
            deposito = request.form['deposito'] # Atrela o valor inserido pelo usuário à variável deposito
            if modelo.validaOperacao(deposito): # Confere se o input do usuário é composto apenas de números e um .
                linhaConta = bd.pegarLinha('conta', 'numero_conta', session['numero_conta'])
                saldoAntes = linhaConta['saldo_conta'] #Guardando o valor do saldo antes da operação
                dataHora = modelo.dataHora(True) #Armazenando data e hora do sistema na variável dataHora
                dic_dados = {'numero_conta': session['numero_conta'], 'numero_agencia':session['numero_agencia'],'valor': deposito, 'dataHora': dataHora, 'saldoAntes': saldoAntes, 'operacao': 'Depósito', 'status_operacao': 'Pendente'} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
                bd.inserirOperacao('historico_operacao', 'Depósito', dic_dados) #Guardando operação na tabela histórico do banco de dados
                #bd.reqDeposito(dic_dados) #Guardando operação na tabela histórico do banco de dados '''
                session['dic_dados'] = dic_dados
                flash('Requisição de depósito enviada.', 'info') # Mensagem para indicar que a operação deu certo
                return redirect(url_for('comprovante', origem = 'operacao', operacao = 'deposito', id = '0')) # Redirecionando para a tela home
            else:
                flash('Insira apenas números e use "." para separar reais de centavos.' 'info') # Mensagem de que o input não é válido
                return redirect(url_for('deposito')) # recarrega a página

        else:
            return render_template('deposito.html', saldo = bd.consultaSaldo(session['id_usuario']), gerente = session['gerente']) # Reenderização do template
    else:
        return redirect(url_for('login')) 


@app.route('/saque', methods = ['POST', 'GET'])
def saque():
    if 'nome' in session: # Se o usuário não está logado, retorna para a tela de login, caso contrário reenderiza a tela de depósito
        if request.method == 'POST':
            saque = request.form['saque'] # Atrela o valor inserido pelo usuário à variável saque
            if modelo.validaOperacao(saque): # Confere se o input do usuário é composto apenas de números e um .
                linhaConta = bd.pegarLinha('conta', 'numero_conta', session['numero_conta'])
                saldoAntes = linhaConta['saldo_conta'] #Guardando o valor do saldo antes da operação
                ct = bd.pegarLinha('capital_banco', 'id_capital', 0)
                ct = ct['capital_total']
                if int(float(saque)) <= ct:
                    modelo.saque(session['id_usuario'], saque) # Atualiza o saldo do usuário com o novo valor
                    dataHora = modelo.dataHora(True) #Armazenando data e hora do sistema na variável dataHora
                    dic_dados = {'numero_conta': session['numero_conta'], 'numero_agencia':session['numero_agencia'],'valor': saque, 'dataHora': dataHora, 'saldoAntes': saldoAntes, 'operacao': 'Saque', 'status_operacao': 'Aprovado'} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
                    bd.inserirOperacao('historico_operacao', 'Saque', dic_dados) #Guardando operação na tabela histórico do banco de dados
                    modelo.atualizaCapital()
                    session['dic_dados'] = dic_dados
                    flash('Saque realizado com sucesso.', 'info') # Mensagem para indicar que a operação deu certo
                    return redirect(url_for('comprovante', origem = 'operacao', operacao = 'saque', id = '0')) # Redirecionando para a tela home
                else:
                    flash('Não podemos realizar essa operação no momento, tente mais tarde', 'info') # Mensagem de que o input não é válido
                    return redirect(url_for('saque')) # recarrega a página
            else:
                flash('Insira apenas números e use "." para separar reais de centavos. Não são aceitos números com mais de 6 caracteres antes do ponto.', 'info') # Mensagem de que o input não é válido
                return redirect(url_for('saque')) # recarrega a página
        else:
            return render_template('saque.html', saldo = bd.consultaSaldo(session['id_usuario']), gerente = session['gerente']) # Reenderização do template
            
    else:
        return redirect(url_for('login'))


@app.route('/transferencia', methods = ['POST', 'GET'])
def transferencia():
    if 'nome' in session:
        if request.method == 'POST':
            transferencia = request.form['transferencia']
            numero_recebedor = request.form['numero']
            if modelo.validaOperacao(transferencia):
                linhaContaEnvio = bd.pegarLinha('conta', 'numero_conta', session['numero_conta'])
                saldoAntesEnvio = linhaContaEnvio['saldo_conta'] #Guardando o valor do saldo antes da operação
                linhaContaRecebido = bd.pegarLinha('conta', 'numero_conta', numero_recebedor)
                dadosContaRecebido = bd.pegarLinha('usuario', 'id_usuario', linhaContaRecebido['id_usuario'])
                if modelo.transferencia(session['id_usuario'], transferencia, numero_recebedor):
                    dataHora = modelo.dataHora(True) #Armazenando data e hora do sistema na variável dataHora
                    dic_dados = {'numero_conta': session['numero_conta'], 'operacao': 'Transferencia', 'valor': transferencia, 'dataHora': dataHora, 'saldoAntes': saldoAntesEnvio, 'contaDestino': numero_recebedor, 'saldoAntesRecebedor': linhaContaRecebido['saldo_conta'], 'numero_agencia_recebedor': linhaContaRecebido['numero_agencia'], 'status_operacao': 'Aprovado', 'numero_agencia':session['numero_agencia'], 'nome_destino': dadosContaRecebido['nome_usuario']} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
                    bd.inserirOperacaoTransferencia('historico_operacao', 'Transferencia', dic_dados) #Guardando operação na tabela histórico do banco de dados '''
                    session['dic_dados'] = dic_dados
                    flash('transferencia realizada com sucesso', 'info')
                    return redirect(url_for('comprovante', origem = 'operacao', operacao = 'transferencia', id = '0'))
                else:
                    flash('Número de conta invalido', 'erro')
                    return redirect(url_for('transferencia'))
            else:
                flash('Insira apenas números e use "." para separar reais de centavos.', 'info') # Mensagem de que o input não é válido
                return redirect(url_for('transferencia')) # recarrega a página
        else:
            return render_template('transferencia.html', gerente = session['gerente'])
    else:
        return redirect(url_for('login'))


@app.route('/comprovante/<origem>/<operacao>/<id>') #Gerador de comprovante
def comprovante(origem, operacao, id):
    if origem == 'operacao':
        if operacao == 'transferencia':
            return render_template('comprovante.html', nome = session['nome'], info = bd.pegarLinha('historico_operacao', 'data_hora_operacao', session['dic_dados']['dataHora']), nome_destino = session['dic_dados']['nome_destino'], gerente = session['gerente'], origem = origem)
        elif operacao == 'deposito' or 'saque':
            return render_template('comprovante.html', nome = session['nome'], info = bd.pegarLinha('historico_operacao', 'data_hora_operacao', session['dic_dados']['dataHora']), gerente = session['gerente'], origem = origem)
    else:
        if operacao == 'transferencia':
            info = bd.pegarLinha('historico_operacao', 'id_operacao', id)
            contaDestino = bd.pegarLinha('conta', 'numero_conta', info['numero_conta_destino'])
            contaOrigem = bd.pegarLinha('conta', 'numero_conta', info['numero_conta'])
            pessoaDestino = bd.pegarLinha('usuario', 'id_usuario', contaDestino['id_usuario'])
            pessoaOrigem = bd.pegarLinha('usuario', 'id_usuario', contaOrigem['id_usuario'])
            return render_template('comprovante.html', nome = session['nome'], info = info , gerente = session['gerente'], origem = origem, pessoaDestino = pessoaDestino, pessoaOrigem = pessoaOrigem)
        else:
            return render_template('comprovante.html', nome = session['nome'], info = bd.pegarLinha('historico_operacao', 'id_operacao', id), gerente = session['gerente'], origem = origem)


@app.route('/extrato', methods = ['GET', 'POST'])
def extrato():
    if request.method == 'POST':
        periodo = request.form
        operacoes = bd.extratoPersonalizado(session['numero_conta'], periodo['data_inicio'], periodo['data_fim'])
        dic_nome_conta_origem = modelo.dadosTransferenciaOrigem(operacoes)
        dic_nome_conta_destino = modelo.dadosTransferenciaDestino(operacoes)
        return render_template('extrato.html', nome = session['nome'], numero_conta = session['numero_conta'], numero_agencia = session['numero_agencia'], operacoes = operacoes, dic_nome_conta_destino = dic_nome_conta_destino, dic_nome_conta_origem = dic_nome_conta_origem, gerente = session['gerente'])
    else:
        operacoes = bd.extrato(session['numero_conta'])
        dic_nome_conta_origem = modelo.dadosTransferenciaOrigem(operacoes)
        dic_nome_conta_destino = modelo.dadosTransferenciaDestino(operacoes)
        return render_template('extrato.html', nome = session['nome'], numero_conta = session['numero_conta'], numero_agencia = session['numero_agencia'], operacoes = operacoes, dic_nome_conta_destino = dic_nome_conta_destino, dic_nome_conta_origem = dic_nome_conta_origem, gerente = session['gerente'])


#tentativa de fazer pdf
'''@app.route('/geraPDF/<tipo>') #gerador de PDF
def geraPDF(tipo):
    if tipo == comprovante:
        render = render_template('comprovante.html', nome = session['nome'], numero_conta = session['numero_conta'], saldoAntes = session['dic_dados']['saldoAntes'], operacao = session['dic_dados']['operacao'], valor = session['dic_dados']['valor'], dataHora =session['dic_dados']['dataHora'])
    else:
        render = render_template('extrato.html', nome = session['nome'], numero_conta = session['numero_conta'], saldoAntes = session['dic_dados']['saldoAntes'], operacao = session['dic_dados']['operacao'], valor = session['dic_dados']['valor'], dataHora =session['dic_dados']['dataHora'])
    dataHora = session['dic_dados']['dataHora'] 
    pdf = pdfkit.from_string(render, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {tipo}_{dataHora}.pdf'
    return response'''

#======================================= Rotas extritamente funcionais (sem html) =======================================


# Rota de loggout. Ela não reenderiza nenhum html, apenas limpa as informações da session e redireciona para o login.
@app.route('/loggout')
def loggout():
    if 'nome' in session: # Se a pessoa estiver logada (nome está na session)
        nome = session['nome'] # Passando o nome para uma variável para transmitir para a mensagem
        flash(f'{nome}, você saiu da sua conta com sucesso.', 'info') # Criando uma mensagem que vai ser mostrada na pagina login
    session.pop(all, None) # Apagando as informações armazenadas na session['nome']
    if session['gerente'] != 'nao':
        return redirect(url_for('login')) # Redireciona para o login.
    else:
        return redirect(url_for('loginGerente'))

#Envia requisição de encerramento de conta
@app.route("/enviaReqEncerramento")
def enviaReqEncerramento():
    if 'nome' in session:
        linhaConta = bd.pegarLinha('conta', 'numero_conta', session['numero_conta'])
        saldo = linhaConta['saldo_conta']
        bd.reqFecha(session['id_usuario'], linhaConta['numero_agencia'], saldo)
        flash('Requisição de fechamento de conta enviada.')
        if session['gerente'] != 'nao':
            return redirect(url_for('homeGerenteAgencia'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login')) # Redireciona para o login.




#======================================= Requisições do Usuário =======================================

@app.route('/reqMudancaCadastral', methods=['POST', 'GET'])
def mudancaCadastral():
    if request.method == 'POST':
        form = request.form
        bd.reqMudanca(form, session['id_usuario'], session['numero_agencia'])
        flash('Requisição de mudança cadastral enviada.')
        if session['gerente'] == 'agencia':
            return redirect(url_for('homeGerenteAgencia'))
        else:
            return redirect(url_for('home'))
    else:
        linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', session['id_usuario'])
        return render_template('user.html', linhaUsuario = linhaUsuario, gerente = session['gerente'], alteracao = False)

'''@app.route('/reqEncerramento')
def reqEncerramento():
    return render_template('encerramentoConta.html')'''


#======================================= Requisições para o gerente =======================================

@app.route('/requisicoes/<tipo>') #nome das tabelas (possíveis valores do tipo): confirmacao_deposito, alteracao_cadastral, encerramento_conta, confirmacao_cadastro
def requisicoes(tipo):
    usuario = bd.pegarTabela('usuario')
    conta = bd.pegarTabela('conta')
    return render_template('requisicoes.html', 
    requisicoes = bd.tabelaPersonalizada(str(tipo), 'numero_agencia', session['numero_agencia']), tipo = tipo, tabelaUsuario = usuario, tabelaConta = conta, gerente = session['gerente'])


@app.route('/resposta/<decisao>/<tipo>/<id>')
def respostaReq(decisao, tipo, id):
    if tipo == 'historico_operacao':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('historico_operacao', 'id_operacao', id)
            linhaConta = bd.pegarLinha('conta', 'numero_conta', linhaOperacao['numero_conta'])
            dataHora = modelo.dataHora(True)
            modelo.deposito(linhaConta['id_usuario'], linhaOperacao['valor_operacao'])
            modelo.atualizaCapital()
            bd.atualizaDeposito(tipo, dataHora, 'Aprovado', id)
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))
        else:
            dataHora = modelo.dataHora(True)
            bd.atualizaDeposito(tipo, dataHora, 'Negado', id)
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))
    
    elif tipo == 'confirmacao_cadastro':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('confirmacao_cadastro', 'id_cadastro', id)
            dataHora = modelo.dataHora(False)
            bd.criaConta(linhaOperacao, dataHora)
            bd.apaga_linha(tipo, 'id_cadastro', id) #Deleta linha na tabela confirmacao cadastro
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))
        else:
            bd.apaga_linha(tipo, 'id_cadastro', id) #Deleta linha na tabela confirmacao cadastro
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))
    
    elif tipo == 'alteracao_cadastral':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('alteracao_cadastral', 'id_alteracao', id)
            if linhaOperacao['nome_alteracao'] != session['nome']:
                session['nome'] = linhaOperacao['nome_alteracao']
            modelo.alteraPorRequisicao(linhaOperacao['id_usuario'])
            bd.apaga_linha(tipo, 'id_alteracao', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))
        else:
            bd.apaga_linha(tipo, 'id_alteracao', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))

    elif tipo == 'encerramento_conta':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('encerramento_conta', 'id_encerramento', id)
            linhaConta = bd.pegarLinha('conta', 'id_usuario', linhaOperacao['id_usuario'])
            modelo.apagaUsuario(linhaConta['numero_conta'], linhaOperacao['id_usuario'])
            bd.apaga_linha(tipo, 'id_encerramento', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))
        else:
            bd.apaga_linha(tipo, 'id_encerramento', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo, gerente = session['gerente']))


#======================================= Gerenciando Usuários da agência =======================================

@app.route('/usuarios_agencia')
def usuarios_agencia():
    tabelaUsuario = bd.pegarTabela('usuario')
    tabelaConta = bd.pegarTabela('conta')
    return render_template('usuarios_agencia.html', usuario = tabelaUsuario, conta = tabelaConta, agencia = session['numero_agencia'], gerente = session['gerente'])

@app.route('/alteracaoGerente/<id_usuario>', methods=['POST', 'GET'])
def alteracaoGerente(id_usuario):
    if request.method == 'POST':
        form = request.form
        modelo.alteraPorGerente(form, id_usuario)
        return redirect(url_for(f'alteracaoGerente', id_usuario = id_usuario))
    else:
        linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', id_usuario)
        return render_template('user.html', linhaUsuario = linhaUsuario, gerente = session['gerente'], id_usuario = id_usuario, alteracao = True)
        
        
@app.route('/encerraConta/<id_usuario>', methods=['POST', 'GET'])
def encerraConta(id_usuario):
    linhaConta = bd.pegarLinha('conta', 'id_usuario', id_usuario)
    modelo.apagaUsuario(linhaConta['numero_conta'], id_usuario)
    return redirect(url_for('usuarios_agencia'))
        

#======================================= Rotas de gerente geral =======================================

@app.route('/agencias')
def agencias():
    tabelaAgencia = bd.pegarTabela('agencia')
    tabelaUsuario = bd.pegarTabela('usuario')
    tabelaGerente = bd.pegarTabela('gerente_geral')
    return render_template('agencias.html', tabelaAgencia = tabelaAgencia, tabelaUsuario = tabelaUsuario, tabelaGerente = tabelaGerente)

@app.route('/usuariosAgencia/<numero_agencia>')
def usuariosAgencia(numero_agencia):
    tabelaUsuario = bd.pegarTabela('usuario')
    tabelaConta = bd.pegarTabela('conta')
    agencia = int(numero_agencia)
    return render_template('usuarios_agencia.html', usuario = tabelaUsuario, conta = tabelaConta, agencia = agencia, gerente = session['gerente'])

@app.route('/alteraAgencia/<numero_agencia>', methods = ['POST', 'GET'])
def alteraAgencia(numero_agencia):
    linhaAgencia =bd.pegarLinha('agencia','numero_agencia', numero_agencia)
    linhaGerente = bd.pegarLinha('gerente_geral', 'numero_matricula', linhaAgencia['numero_matricula'])
    linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', linhaGerente['id_usuario'])
    numero_agencia = int(numero_agencia)
    if request.method == 'POST':
        form = request.form
        
        if modelo.atualizaNumeroAgencia(form, numero_agencia):
            flash('alteração realizada com sucesso')
            return redirect(url_for('alteraAgencia', numero_agencia = form['numero_agencia']))
        else:
            flash('esse número de agencia já existe')
            return redirect(url_for('alteraAgencia', numero_agencia = numero_agencia))
    else:
        return render_template('alteraAgencia.html', agencia = numero_agencia, linhaAgencia = linhaAgencia, linhaGerente = linhaGerente, linhaUsuario =linhaUsuario)


@app.route('/alteraGerente/<id_usuario>', methods = ['POST', 'GET'])
def mudaGerente(id_usuario):
    linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', id_usuario)
    linhaGerente = bd.pegarLinha('gerente_geral', 'id_usuario', id_usuario)
    linhaAgencia = bd.pegarLinha('agencia', 'numero_matricula', linhaGerente['numero_matricula'])
    if request.method == 'POST':
        form = request.form
        if form['numero_matricula'] == '':
            modelo.alteraPorGerente(form,id_usuario)
            return redirect(url_for('mudaGerente', id_usuario = id_usuario))
        else:
            modelo.alteraPorGerente(form, id_usuario)
            bd.mudaMatricula(form['numero_matricula'], linhaGerente['numero_matricula'])
            return redirect(url_for('mudaGerente', id_usuario = id_usuario))
    else:
        return render_template('alteraGerente.html', linhaUsuario = linhaUsuario, linhaGerente = linhaGerente, linhaAgencia =linhaAgencia)


@app.route('/criaAgencia')
def criaAgencia():
    return render_template('criaAgencia.html')

if __name__ == '__main__':
    app.run(debug = True)