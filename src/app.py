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
    if 'nome' in session: #Verificando se a pessoa já está logada
        return redirect(url_for('home'))
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
        data = modelo.dataHora(False)
        bd.criaConta(dadosCliente, data) #Insere os valores do formulário na tabela cliente
        id = bd.pegarLinha('usuario', 'cpf_usuario', dadosCliente['CPF'])
        linhaConta = bd.pegarLinha('conta', 'id_usuario', id['id_usuario']) # Pegando a linha da conta para acessar o numero da conta na linha seguinte
        numero_conta = linhaConta['numero_conta'] # Guardando numero_usuario para ser usado em outras telas
        flash(f'Conta criada com sucesso.' ) # Mensagem que informa qual o número do usuário
        flash(f'O seu número de conta é: {numero_conta}.')
        flash(f'Ele será necessário para acessar sua conta.')
            
        return redirect(url_for('login'))

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
            return render_template('homegerente.html')
    else:
        return redirect(url_for('login'))

# Rota de loggout. Ela não reenderiza nenhum html, apenas limpa as informações da session e redireciona para o login.
@app.route('/loggout')
def loggout():
    if 'nome' in session: # Se a pessoa estiver logada (nome está na session)
        nome = session['nome'] # Passando o nome para uma variável para transmitir para a mensagem
        flash(f'{nome}, você saiu da sua conta com sucesso.', 'info') # Criando uma mensagem que vai ser mostrada na pagina login
    session.pop(all, None) # Apagando as informações armazenadas na session['nome']
    return redirect(url_for('login')) # Redireciona para o login.



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
                dic_dados = {'numero_conta': session['numero_conta'], 'operacao': 'saque', 'valor': saque, 'dataHora': dataHora, 'saldoAntes': saldoAntes, 'contaDestino': None} #Colocando os dados necessários para a chamada da função inserirOperação em uma variável dicionário
                '''bd.inserirOperacao('HistoricoOperacao', dic_dados) #Guardando operação na tabela histórico do banco de dados '''
                session['dic_dados'] = dic_dados
                flash('Saque realizado com sucesso. ', 'info') # Mensagem para indicar que a operação deu certo
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
                if modelo.transferencia(session['id_usuario'], transferencia, numero_recebedor):
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

if __name__ == '__main__':
    app.run(debug = True)