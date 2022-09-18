from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_mysqldb import MySQL
import bd, modelo # Importando os outros arquivos .py

app = Flask(__name__)
app.secret_key = 'aonainfinnBFNFOANOnasfononfsa' #Chave de segurança da session

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' #Insira aqui a senha do seu servidor local do MYSQL
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
        if not bd.valida('usuario', 'cpf_usuario', dadosCliente['cpf']): #validação cpf
            bd.criaConta(dadosCliente) #Insere os valores do formulário na tabela cliente
            id = bd.pegarLinha('usuario', 'cpf_usuario', dadosCliente['cpf'])
            linhaConta = bd.pegarLinha('conta', 'id_usuario', id['id_usuario']) # Pegando a linha da conta para acessar o numero da conta na linha seguinte
            numero_conta = linhaConta['numero_conta'] # Guardando numero_usuario para ser usado em outras telas
            flash(f'Conta criada com sucesso.' ) # Mensagem que informa qual o número do usuário
            flash(f'O seu número de conta é: {numero_conta}.')
            flash(f'Ele será necessário para acessar sua conta.')
            
            return redirect(url_for('login'))
        else:
            flash('Este CPF já está cadastrado')
            return redirect(url_for('cadastro'))
    else:
        return render_template('cadastro.html')


# Rota da página home
@app.route('/home')
def home():
    return render_template('home.html', nome = session['nome'],
    saldo = bd.consultaSaldo(session['id_usuario']),
    numero_conta = str(session['numero_conta']))


# Rota de loggout. Ela não reenderiza nenhum html, apenas limpa as informações da session e redireciona para o login.
@app.route('/loggout')
def loggout():
    if 'nome' in session: # Se a pessoa estiver logada (nome está na session)
        nome = session['nome'] # Passando o nome para uma variável para transmitir para a mensagem
        flash(f'{nome}, você saiu da sua conta com sucesso.', 'info') # Criando uma mensagem que vai ser mostrada na pagina login
    session.pop('nome', None) # Apagando as informações armazenadas na session['nome']
    return redirect(url_for('login')) # Redireciona para o login.


@app.route('/deposito', methods = ['POST', 'GET'])
def deposito():
    if 'nome' in session: # Se o usuário não está logado, retorna para a tela de login, caso contrário reenderiza a tela de depósito
        if request.method == 'POST':
            deposito = request.form['deposito'] # Atrela o valor inserido pelo usuário à variável deposito
            atual = bd.consultaSaldo(session['id_usuario']) # Atrela o saldo atual do usuário à variável atual
            if modelo.validaOperacao(deposito): # Confere se o input do usuário é composto apenas de números e um .
                deposito = float(deposito) # Transforma a string deposito em float
                atual = atual + deposito # Realiza a soma dos valores
                bd.mudaSaldo(atual, session['id_usuario']) # Atualiza o saldo do usuário com o novo valor
                flash('Depósito realizado com sucesso.', 'info') # Mensagem para indicar que a operação deu certo
                return redirect(url_for('home')) # Redirecionando para a tela home
            else:
                flash('Insira apenas números e use "." para separar reais de centavos. Não são aceitos números com mais de 6 caracteres antes do ponto.', 'info') # Mensagem de que o input não é válido
                return redirect(url_for('deposito')) # recarrega a página

        else:
            return render_template('deposito.html') # Reenderização do template
    else:
        return redirect(url_for('login')) 


@app.route('/saque', methods = ['POST', 'GET'])
def saque():
    if 'nome' in session: # Se o usuário não está logado, retorna para a tela de login, caso contrário reenderiza a tela de depósito
        if request.method == 'POST':
            saque = request.form['saque'] # Atrela o valor inserido pelo usuário à variável saque
            atual = bd.consultaSaldo(session['id_usuario']) # Atrela o saldo atual do usuário à variável atual
            if modelo.validaOperacao(saque): # Confere se o input do usuário é composto apenas de números e um .
                saque = float(saque) # Transforma a string deposito em float
                atual = atual - saque # Realiza a soma dos valores
                bd.mudaSaldo(atual, session['id_usuario']) # Atualiza o saldo do usuário com o novo valor
                flash('Saque realizado com sucesso.', 'info') # Mensagem para indicar que a operação deu certo
                return redirect(url_for('home')) # Redirecionando para a tela home
            else:
                flash('Insira apenas números e use "." para separar reais de centavos. Não são aceitos números com mais de 6 caracteres antes do ponto.', 'info') # Mensagem de que o input não é válido
                return redirect(url_for('saque')) # recarrega a página
        else:
            return render_template('saque.html') # Reenderização do template
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug = True)