from flask import Flask
from flask_mysqldb import MySQL
import bd


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Goiabada2!'
app.config['MYSQL_DB'] = 'banco'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

def validaOperacao(input):
    if '.' in input:
        controle = input.split('.')
        if len(controle) > 2:
            return False
        elif controle[0].isnumeric() and controle[1].isnumeric():
            return True
        else:
            return False
    elif input.isnumeric():
        return True
    else:
        return False



