from asyncio.windows_events import NULL
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
            session['nome'] = linhaUsuario['nome_usuario'] # Guardando nome_usuario para ser usado em outras telas
            session['id_usuario'] = linhaUsuario['id_usuario'] # Guardando id_usuario para ser usado em outras telas
            session['numero_conta'] = linhaConta['numero_conta'] # Guardando numero_usuario para ser usado em outras telas
            session['numero_agencia'] = linhaConta['numero_agencia']
            return redirect(url_for('home')) # Redirecionando para tela home
        else:
            flash("Número da Conta ou Senha incorretos", "info")
            return redirect(url_for('login'))
        
    else:
        return render_template('login.html')


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


# Rota da página home
@app.route('/home')
def home():
    if 'nome' in session:
        if 'dic_dados' in session: #Se há algum dado de operação na session, ele será apagado.
            session.pop('dic_dados', None)
        if not bd.valida('gerente_agencia', 'id_usuario', session['id_usuario']):
            return render_template('home.html', nome = session['nome'],
            saldo = bd.consultaSaldo(session['id_usuario']),
            numero_conta = str(session['numero_conta']))
        else:
            return render_template('homegerente.html', nome = session['nome'],
            saldo = bd.consultaSaldo(session['id_usuario']),
            numero_conta = str(session['numero_conta']))
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
                dic_dados = {'numero_conta': session['numero_conta'], 'numero_agencia':session['numero_agencia'],'valor': deposito, 'dataHora': dataHora, 'saldoAntes': saldoAntes, 'operacao': 'deposito'} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
                bd.reqDeposito(dic_dados) #Guardando operação na tabela histórico do banco de dados '''
                session['dic_dados'] = dic_dados
                flash('Requisição de depósito enviada.', 'info') # Mensagem para indicar que a operação deu certo
                return redirect(url_for('comprovante')) # Redirecionando para a tela home
            else:
                flash('Insira apenas números e use "." para separar reais de centavos.' 'info') # Mensagem de que o input não é válido
                return redirect(url_for('deposito')) # recarrega a página

        else:
            return render_template('deposito.html', saldo = bd.consultaSaldo(session['id_usuario'])) # Reenderização do template
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
                modelo.saque(session['id_usuario'], saque) # Atualiza o saldo do usuário com o novo valor
                dataHora = modelo.dataHora(True) #Armazenando data e hora do sistema na variável dataHora
                dic_dados = {'numero_conta': session['numero_conta'], 'operacao': 'saque', 'valor': saque, 'dataHora': dataHora, 'saldoAntes': saldoAntes} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
                bd.inserirOperacao('historico_operacao', 'saque', dic_dados) #Guardando operação na tabela histórico do banco de dados
                session['dic_dados'] = dic_dados
                flash('Saque realizado com sucesso.', 'info') # Mensagem para indicar que a operação deu certo
                return redirect(url_for('comprovante')) # Redirecionando para a tela home
            else:
                flash('Insira apenas números e use "." para separar reais de centavos. Não são aceitos números com mais de 6 caracteres antes do ponto.', 'info') # Mensagem de que o input não é válido
                return redirect(url_for('saque')) # recarrega a página
        else:
            return render_template('saque.html', saldo = bd.consultaSaldo(session['id_usuario'])) # Reenderização do template
            
    else:
        return redirect(url_for('login'))


@app.route('/transferencia', methods = ['POST', 'GET'])
def transferencia():
    if 'nome' in session:
        if request.method == 'POST':
            transferencia = request.form['transferencia']
            numero_recebedor = request.form['numero']
            if modelo.validaOperacao(transferencia):
                linhaConta = bd.pegarLinha('conta', 'numero_conta', session['numero_conta'])
                saldoAntes = linhaConta['saldo_conta'] #Guardando o valor do saldo antes da operação
                if modelo.transferencia(session['numero_conta'], transferencia, numero_recebedor):
                    dataHora = modelo.dataHora(True) #Armazenando data e hora do sistema na variável dataHora
                    dic_dados = {'numero_conta': session['numero_conta'], 'operacao': 'transferencia', 'valor': transferencia, 'dataHora': dataHora, 'saldoAntes': saldoAntes, 'contaDestino': numero_recebedor} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
                    '''bd.inserirOperacao('HistoricoOperacao', dic_dados) #Guardando operação na tabela histórico do banco de dados '''
                    session['dic_dados'] = dic_dados
                    flash('transferencia realizada com sucesso', 'info')
                    return redirect(url_for('comprovante'))
                else:
                    flash('Número de conta invalido', 'erro')
                    return redirect(url_for('transferencia'))
            else:
                flash('Insira apenas números e use "." para separar reais de centavos. Não são aceitos números com mais de 6 caracteres antes do ponto.', 'info') # Mensagem de que o input não é válido
                return redirect(url_for('transferencia')) # recarrega a página
        else:
            return render_template('transferencia.html')
    else:
        return redirect(url_for('login'))


@app.route('/comprovante') #Gerador de comprovante
def comprovante():
    return render_template('comprovante.html', nome = session['nome'], numero_conta = session['numero_conta'], saldoAntes = session['dic_dados']['saldoAntes'], operacao = session['dic_dados']['operacao'], valor = session['dic_dados']['valor'], dataHora =session['dic_dados']['dataHora'])

@app.route('/extrato')
def extrato():
    dic_dados = bd.tabelaPersonalizada('historico_operacao', 'numero_conta', session['numero_conta'])
    a = session['numero_conta']
    return render_template('extrato.html', operacoes = dic_dados, numero_conta = session['numero_conta'], nome = session['nome'])



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
    return redirect(url_for('login')) # Redireciona para o login.

#Envia requisição de encerramento de conta
@app.route("/enviaReqEncerramento")
def enviaReqEncerramento():
    if 'nome' in session:
        linhaConta = bd.pegarLinha('conta', 'numero_conta', session['numero_conta'])
        saldo = linhaConta['saldo_conta']
        bd.reqFecha(session['id_usuario'], linhaConta['numero_agencia'], saldo)
        flash('Requisição de fechamento de conta enviada.')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login')) # Redireciona para o login.



#======================================= Requisições do Usuário =======================================

@app.route('/mudancaCadastral', methods=['POST', 'GET'])
def mudancaCadastral():
    if request.method == 'POST':
        form = request.form
        bd.reqMudanca(form, session['id_usuario'], session['numero_agencia'])
        flash('Requisição de mudança cadastral enviada.')
        return redirect(url_for('home'))
    else:
        linhaUsuario = bd.pegarLinha('usuario', 'id_usuario', session['id_usuario'])
        return render_template('user.html', linhaUsuario = linhaUsuario)

'''@app.route('/reqEncerramento')
def reqEncerramento():
    return render_template('encerramentoConta.html')'''


#======================================= Requisições para o gerente =======================================

@app.route('/requisicoes/<tipo>') #nome das tabelas (possíveis valores do tipo): confirmacao_deposito, alteracao_cadastral, encerramento_conta, confirmacao_cadastro
def requisicoes(tipo):
    return render_template('requisicoes.html', 
    requisicoes = bd.tabelaPersonalizada(str(tipo), 'numero_agencia', session['numero_agencia']), tipo = tipo)


@app.route('/resposta/<decisao>/<tipo>/<id>')
def respostaReq(decisao, tipo, id):
    if tipo == 'confirmacao_deposito':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('confirmacao_deposito', 'id_confirmacao_deposito', id)
            linhaConta = bd.pegarLinha('conta', 'numero_conta', linhaOperacao['numero_conta'])
            saldoAtual = linhaConta['saldo_conta']
            dataHora = modelo.dataHora(True)
            dic_dados = {'numero_conta': linhaOperacao['numero_conta'], 'operacao': 'deposito', 'valor': linhaOperacao['valor_confirmacao_deposito'], 'dataHora': dataHora, 'saldoAntes': saldoAtual}
            modelo.deposito(linhaConta['id_usuario'], linhaOperacao['valor_confirmacao_deposito'])
            bd.inserirOperacao('historico_operacao', 'deposito', dic_dados)
            bd.apaga_linha(tipo, 'id_confirmacao_deposito', id) #Deleta linha na tabela confirmacao depósito
            return redirect(url_for('requisicoes', tipo=tipo))
        else:
            bd.apaga_linha(tipo, 'id_confirmacao_deposito', id) #Deleta linha na tabela confirmacao depósito
            return redirect(url_for('requisicoes', tipo=tipo))
    
    elif tipo == 'confirmacao_cadastro':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('confirmacao_cadastro', 'id_cadastro', id)
            dataHora = modelo.dataHora(False)
            bd.criaConta(linhaOperacao, dataHora)
            bd.apaga_linha(tipo, 'id_cadastro', id) #Deleta linha na tabela confirmacao cadastro
            return redirect(url_for('requisicoes', tipo=tipo))
        else:
            bd.apaga_linha(tipo, 'id_cadastro', id) #Deleta linha na tabela confirmacao cadastro
            return redirect(url_for('requisicoes', tipo=tipo))
    
    elif tipo == 'alteracao_cadastral':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('alteracao_cadastral', 'id_alteracao', id)
            if linhaOperacao['nome_alteracao'] != session['nome']:
                session['nome'] = linhaOperacao['nome_alteracao']
            modelo.alteraCadastro(linhaOperacao['id_usuario'])
            bd.apaga_linha(tipo, 'id_alteracao', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo))
        else:
            bd.apaga_linha(tipo, 'id_alteracao', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo))

    elif tipo == 'encerramento_conta':
        if decisao == 'aceita':
            linhaOperacao = bd.pegarLinha('encerramento_conta', 'id_encerramento', id)
            linhaConta = bd.pegarLinha('conta', 'id_usuario', linhaOperacao['id_usuario'])
            modelo.apagaUsuario(linhaConta['numero_conta'], linhaOperacao['id_usuario'])
            bd.apaga_linha(tipo, 'id_encerramento', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo))
        else:
            bd.apaga_linha(tipo, 'id_encerramento', id) #Deleta linha na tabela alteracao_cadastral
            return redirect(url_for('requisicoes', tipo=tipo))




if __name__ == '__main__':
    app.run(debug = True)