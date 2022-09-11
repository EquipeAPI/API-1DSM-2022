from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_mysqldb import MySQL
import bd

app = Flask(__name__)
app.secret_key = 'aonainfinnBFNFOANOnasfononfsa' #Chave de segurança da session

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Guará'
app.config['MYSQL_PASSWORD'] = 'Guarana2!'
app.config['MYSQL_DB'] = 'teste'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Rota da página de login (que é a página inicial)
@app.route('/', methods=['POST', 'GET']) # As duas rotas acionaram a mesma função
@app.route('/login', methods=['POST', 'GET']) # Colocando os metodos HTTP que serão usados
def login():
    if 'nome' in session: #Verificando se a pessoa já está logada
        return redirect(url_for('home'))
    if request.method == 'POST': #Se a pessoa apertar o botão 'ENTRAR' do forms
        cpf = request.form['cpf'] #Adicionando a uma variável python a informação do input cpf do forms
        senha = request.form['senha'] #Adicionando a uma variável python a informação do input senha do forms
 
        if bd.valida("cliente", "cpf", cpf) and bd.valida("cliente", "senha", senha): #Inserir tabela, coluna, valor para ver se o valor existe na coluna da tabela, se existir retorna True
            nome = bd.pegarLinha("cliente", "cpf", cpf) #Função que retorna os valores da linha da tabela escolhida (tabela, coluna, valor da linha requisitada)
            session['nome'] = nome['nome']
            return redirect(url_for('home'))
        else:
            flash("Senha ou CPF incorretos", "info")
            return redirect(url_for('login'))
        
    else:
        return render_template('login.html')


# Rota da página de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        dadosCliente = request.form # Armazena todos os dados inseridos no formulário em uma variável tipo dicionário
        nome = dadosCliente['nome'] # Armazena o que foi enviado do formulário no input 'nome' numa variável de mesmo nome
        cpf = dadosCliente['cpf'] # Mesmo procedimento para o cpf
        senha = dadosCliente['senha'] # Igualmente para a senha (ainda tenho que aprender a deixar isso de uma forma segura)

        bd.criaConta(nome, cpf, senha) #Insere os valores do formulário na tabela cliente

        return redirect(url_for('login'))
        
    else:
        return render_template('cadastro.html')


# Rota da página home
@app.route('/Home')
def home():
    return render_template('home.html', nome = session['nome'])


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
    if 'nome' in session:
        if request.method == 'POST':
            deposito = request.form['deposito']
            atual = bd.consultaSaldo(session['nome'])
            
            atual = atual + int(deposito)
            bd.mudaSaldo(atual, session['nome'])
            flash('Depósito realizado com sucesso.', 'info')
            return redirect(url_for('home'))


            '''
            ==========Possível inserção da função depósito usando arquivo .py do modelo==========
            modelo.deposito(deposito)
        
            '''
        else:
            return render_template('deposito.html')
    else:
        return redirect(url_for('login'))


@app.route('/saque', methods = ['POST', 'GET'])
def saque():
    if 'nome' in session:
        if request.method == 'POST':
            saque = request.form['saque']
            atual = bd.consultaSaldo(session['nome'])
            atual = atual - int(saque)
            bd.mudaSaldo(atual, session['nome'])
            flash('Saque realizado com sucesso.', 'info')
            return redirect(url_for('home'))
            


            '''
            ==========Possível inserção da função saque usando arquivo .py do modelo==========
            modelo.saque(saque)
        
            '''
        else:
            return render_template('saque.html')
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug = True)