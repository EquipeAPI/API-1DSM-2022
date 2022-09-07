from flask import Flask, render_template, redirect 

app = Flask(__name__)

# Rota da página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota da página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota da página de login
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    debug = True
    app.run()