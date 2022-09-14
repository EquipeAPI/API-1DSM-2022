# API-1DSM-2022
## Sobre o projeto
Criação de um sistema de Internet Banking capaz de gerenciar operações bancárias simples, como depósito, saque e transferência entre usuários. Back-end do projeto desenvolvido em python utilizando o microframework flask e o MySQL para gerenciar o banco de dados.

## Executando a aplicação
Tenha o Python, MySQL instalados
Clone o repositório
No terminal:
```powershell
# Acesse a página do projeto
cd projeto 

# Instale as dependências
``` 
Utilize dos arquivos script .sql para criar a estrutura do banco de dados

```powershell
# Configure as informações do banco de dados de acordo com o seu servidor 
app.config['MYSQL_HOST'] = '' # localhost
app.config['MYSQL_USER'] = '' # Usuário 
app.config['MYSQL_PASSWORD'] = '' # Senha 
app.config['MYSQL_DB'] = '' # Nome do banco de dados
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
```
Execute a aplicação
