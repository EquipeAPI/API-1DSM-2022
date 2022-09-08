from flask import Flask, render_template, redirect, request, session, url_for, flash
#from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'aonainfinnBFNFOANOnasfononfsa' #Chave de segurança da session

'''
# Configurações do banco de dados
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
'''

# Rota da página de login (que é a página inicial)
@app.route('/', methods=['POST', 'GET']) # As duas rotas acionaram a mesma função
@app.route('/login', methods=['POST', 'GET']) # Colocando os metodos HTTP que serão usados
def login():
    '''if 'nome' in session: #Verificando se a pessoa já está logada
        return redirect(url_for(home))'''
    if request.method == 'POST': #Se a pessoa apertar o botão 'ENTRAR' do forms
        nome = request.form['nome'] #Adicionando a uma variável python a informação do input nome do forms
        session['nome'] = nome #Criando uma session para transportar essa informação de maneira segura entre as rotas
        return redirect(url_for('home'))
        '''
        ==========Possível validação usando arquivo .py do modelo==========
        if modelo.validação(nome, senha):
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
        '''

    else:
        return render_template('login.html')


# Rota da página de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        cliente = request.form #Armazena todos os dados inseridos no formulário em uma variável tipo dicionário
        return redirect(url_for('login'))
        '''
        ==========Possível inserção usando arquivo .py do modelo==========
        if modelo.validação(nome, senha):
            return redirect(url_for('home'))
        else:
            flash = ("Senha ou CPF incorretos. Tente outra vez", info) #Mensagem de erro de login (só aparece se a validação falhar)
            return render_template('login.html')
        
        '''
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


@app.route('/deposito', method = ['POST', 'GET'])
def deposito():
    if 'name' in session:
        if request.method == 'POST':
            deposito = request.form['deposito']
            return redirect(url_for('home'))


            '''
            ==========Possível inserção da função depósito usando arquivo .py do modelo==========
            modelo.deposito(deposito)
        
            '''
        else:
            return render_template('deposito.html')
    else:
        return redirect(url_for('login'))


@app.route('/saque', method = ['POST', 'GET'])
def saque():
    if 'name' in session:
        if request.method == 'POST':
            deposito = request.form['saque']
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