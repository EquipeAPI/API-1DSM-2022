from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_mysqldb import MySQL
import bd, modelo

app = Flask(__name__)
app.secret_key = 'aonainfinnBFNFOANOnasfononfsa' #Chave de segurança da session

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Goiabada2!'
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
        cpf = request.form['cpf'] #Adicionando a uma variável python a informação do input cpf do forms
        senha = request.form['senha'] #Adicionando a uma variável python a informação do input senha do forms
 
        if bd.valida("usuario", "cpf_usuario", cpf) and bd.valida("usuario", "senha_usuario", senha): #Inserir tabela, coluna, valor para ver se o valor existe na coluna da tabela, se existir retorna True
            linhaUsuario = bd.pegarLinha("usuario", "cpf_usuario", cpf) #Função que retorna os valores da linha da tabela escolhida (tabela, coluna, valor da linha requisitada)
            session['nome'] = linhaUsuario['nome_usuario']
            session['id_usuario'] = linhaUsuario['id_usuario']
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
        if not bd.valida('usuario', 'cpf_usuario', dadosCliente['cpf']): #validação cpf
            bd.criaConta(dadosCliente) #Insere os valores do formulário na tabela cliente
            return redirect(url_for('login'))

        else:
            flash('Este CPF já está cadastrado')
            return redirect(url_for('cadastro'))

    else:
        return render_template('cadastro.html')


# Rota da página home
@app.route('/Home')
def home():
    return render_template('home.html', nome = session['nome'], saldo = bd.consultaSaldo(session['id_usuario']))


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
            atual = bd.consultaSaldo(session['id_usuario'])
            if modelo.validaOperacao(deposito):
                deposito = float(deposito)
                atual = atual + deposito
                bd.mudaSaldo(atual, session['id_usuario'])
                flash('Depósito realizado com sucesso.', 'info')
                return redirect(url_for('home'))
            else:
                flash('Insira apenas números e use "." para separar reais de centavos')
                return redirect(url_for('deposito'))

        else:
            return render_template('deposito.html')
    else:
        return redirect(url_for('login'))


@app.route('/saque', methods = ['POST', 'GET'])
def saque():
    if 'nome' in session:
        if request.method == 'POST':
            saque = request.form['saque']
            atual = bd.consultaSaldo(session['id_usuario'])
            if modelo.validaOperacao(saque):
                saque = float(saque)
                atual = atual - saque
                bd.mudaSaldo(atual, session['id_usuario'])
                flash('Saque realizado com sucesso.', 'info')
                return redirect(url_for('home'))
            else:
                flash('Insira apenas números e use "." para separar reais de centavos')
                return redirect(url_for('saque'))
        else:
            return render_template('saque.html')
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug = True)