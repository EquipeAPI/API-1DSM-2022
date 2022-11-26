<span id="topo"></span>
<h1 align="center">FATEC Prof Jessen Vidal, São José dos Campos - 1º Semestre DSM 2022</h1>
<p align="center">
    <a href="#sobre">Sobre</a> | 
    <a href="#entregas">Entregas</a> | 
    <a href="#backlogs">Backlogs</a> |  
    <a href="#tecnologias">Tecnologias</a> | 
    <a href="#equipe">Equipe</a> | 
</p>
<span id="sobre"></span>

<h2> Sobre o projeto </h2>
Projeto desenvolvido por alunos do 1º semestre do curso de Desenvolviento de Software Multiplatafora, da FATEC Prof Jessen Vidal em São José dos Campos. <br> Consiste na criação de um sistema de Internet Banking capaz de gerenciar operações bancárias simples, como depósito, saque e transferência entre usuários. Back-end do projeto desenvolvido em python utilizando o microframework flask e o MySQL para gerenciar o banco de dados.
>Status do projeto: Em desenvolvimento :hourglass:

## Como executar a aplicação
* Tenha o Python e o MySQL instalados. <br>
* Clone o repositório. <br>
* No terminal:
```powershell
# Acesse a página do projeto
cd projeto

# Crie um ambiente virtual
python -m venv nomedoambiente

# Ative o ambiente virtual
nomedoambiente/Scripts/activate

# Instale as dependências
pip install -r requirements.txt
``` 
<p>Utilize dos arquivos script .sql para criar a estrutura do banco de dados</p>
<a href="https://www.youtube.com/watch?v=Y18wK0v6mxA">Tutorial em mais detalhes para importar scripts no MySQL</a>

```powershell
# Configure as informações do banco de dados de acordo com o seu servidor nos arquivos app.py e modelo.py 
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = '' # Usuário 
app.config['MYSQL_PASSWORD'] = '' # Senha 
app.config['MYSQL_DB'] = '' # Nome do esquema do banco de dados
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
```
* Execute a aplicação
```powershell
cd src
python app.py
# digite no navegador a url que aparecer no terminal
# padrão: http://127.0.0.1:5000
```

<span id="entregas"></span>

## Entregas
O projeto está sendo realizado utilizando-se da metodologia ágil SCRUM, separadas em 4 entregas com sprints de 21 dias de duração cada uma. <br>

| Sprint| Período | Status |
|:-----:|:----------:|:---------:|
| 01 |   29/08/2022 - 19/09/2022 | Entregue :heavy_check_mark: | 
| 02 |   19/09/2022 - 09/10/2022 | Entregue :heavy_check_mark: |  
| 03 |   10/10/2022 - 06/11/2022 | Entregue :heavy_check_mark: | 
| 04 |   07/11/2022 - 27/11/2022 | Pendente :hourglass:|  

<span id="backlogs"></span>

## Backlogs
### Backlog do produto
| User Story | Requisito |Funcionalidade | Sprint |
| :--:       | :-----------:|:--------------:     |:--:    |
|   | **Protótipo navegável**  |Proposta de arquitetura de informação do sistema| 1 |
|   |  **Cadastro/Login**  | Esquema de abertura de conta. Cadastro, geração de conta e acesso à ela.  | 1 |
| **10** | **RF3.d** | Simulação de depósito.| 1 |
| **11** | **RF3.e** | Simulação de saque.   | 1 |
| **18**  | **RF8**   | Operações bancárias são feitas utilizando duas casas decimais. | 1 |
| **02** | **RF2.a** | Gerentes de Agência autorizam abertura contas atreladas à sua agência.| 2 |
| **03**, **04** | **RF2.b** | Gerentes de Agência autorizam encerraramento de contas atreladas à sua agência.|  2|
| **05** | **RF2.c** | Gerentes de Agência autorizam modificações de dados cadastrais de contas atreladas à sua agência. | 2 |  
| **06** | **RF2.d** | Gerentes de Agência confirmam operações de depósito. | 2 |
| **07** | **RF3.a** | Solicitação de abertura de conta. | 2 |
| **08** | **RF3.b** | Solicitação de encerramento de conta.| 2 |
| **09** | **RF3.c** | Solicitação de alteração de dados cadastrais. | 2 |
| **13** | **RF3.g** | Emissão de extrato da conta. | 2 |
| **14**| **RF3.h**| Emissão de comprovantes de operação. | 2 |
| **01** | **RF1**| O Gerente Geral possui acesso a todas as funcionalidades do sistema.| 3 |
| **12** | **RF3.f**| Transferência entre usuários. | 3 |
| **15** | **RF4**, **RF5** | Operações bancárias alteram o saldo total do banco disponível.|3 |
| **16** | **RF6**| Bloqueio de saques que extrapolem o capital total disponível no banco. | 3 |
| **19** | **RF12** | Saques que extrapolem o saldo disponível da conta deixam o cliente em situação de "cheque especial". | 4 |
| **20** | **RF13** | Clientes em situação de "cheque especial" tem o valor da dívida. automaticamente debitado dos depósitos realizados. | 4 |
| **17** | **RF7** | Truncamento de valores decimais. | 4 |

### Referência das User Stories
| ID | User Stories | 
| :--:       | :-----------:|
| **01** | Como Gerente Geral, eu gostaria de ter acesso irrestrito as funcionalidade do sistema para administrá-lo. |
| **02** | Como Gerente de Agência, eu gostaria de visualizar requisições de cadastro para abrir contas de clientes. |
| **03** | Como Gerente de Agência, eu gostaria de visualizar requisições de encerramento de contas para conferir o saldo e confirmar o fechamento. |
| **04** | Como Gerente de Agência, eu gostaria de visualizar requisições de alteração de dados cadastrais dos meus clientes para aceitar ou recusar a ação.|
| **05**| Como Gerente de Agência, eu gostaria de visualizar depósitos dos meus clientes para conferir e confirmar.|
| **07** | Como usuário comum, eu gostaria de abrir uma conta no banco para utilizar dos serviços.|
| **08** | Como usuário comum, eu gostaria de poder solicitar o encerramento da minha conta para fechar a conta. |
| **09** | Como usuário comum, eu gostaria de poder alterar os dados que eu cadastrei para mantê-los atualizados.|
| **10** | Como usuário comum, eu gostaria de depositar meu dinheiro para guardá-lo ou utilizar em operações do banco.|
| **11** | Como usuário comum, eu gostaria de sacar meu dinheiro para usá-lo em espécie.|
| **12** | Como usuário comum, eu gostaria de transferir quantias para outras contas no mesmo banco para realizar e receber pagamentos. |
| **13** | Como usuário comum, eu gostaria de visualizar o extrato da minha conta para conferir e controlar gastos.|
| **14** | Como usuário comum, eu gostaria que toda operação gerasse um comprovante imediatamente para conferência.|
| **15** | Como Gerente Geral, eu gostaria que operações realizadas no banco alterassem automáticamente o saldo total para evitar inconsistências. |
| **16** | Como Gerente Geral, eu gostaria que o sistema bloqueasse saques de quantias maior do que o capita total do banco disponível para evitar endividamento.|
| **17** | Como Gerente Geral, eu gostaria que fosse realizado o truncamento dos valores decimais no banco para evitar inconsistência de dados.|
| **18** | Como Gerente Geral, eu gostaria que as operações no banco fossem realizadas em duas casas decimais para possibilitar o uso de centavos.|
| **19** | Como Gerente Geral, eu gostaria que clientes que saquem mais do que possuem na conta entrem em situação de cheque especial, para cobrar taxas e júros da dívida.|
| **20** | Como Gerente Geral, eu gostaria de debitar automaticamente de depósitos de clientes que estejam em situação de cheque especial, para automatizar o processo.|

### Backlog das sprints
#### Sprint 1
| Item | Funcionalidade                  |
| :--: | :------------------------- |
|  01  | Organização dos Requisitos|
|  02  | Protótipo Navegável |
|  04  | Cadastro e Login de usuários (Abertura de conta) |
|  05  | Operações de depósito e saque |
<p align="center">
    <img src="docs/entregas/sprint-1/mvp-sprint1.gif">
</p>

### Sprint 2 
| Item | Funcionalidade             |
| :--: | :------------------------- |
|  01  | Criação de Gerentes de Agência|
|  02  | Requisições de cadastro, operações, alterações e encerramento de conta |
|  04  | Controle de requisições do Gerente de Agência |
|  05  | Comprovantes de operações |
|  06  | Extrato de movimentação da conta |
<p align="center">
    <img src="docs/entregas/sprint-2/demo-api-2sprint.gif">
</p>

### Sprint 3 
| Item | Funcionalidade             |
| :--: | :------------------------- |
|  01  | Criação do Gerente Geral|
|  02  | O Gerente Geral possui acesso a todas funcionalidade do sistema, sem restrição. |
|  04  | Funcionalidade de Capital Total |
|  05  | Transferência entre usuários do banco |
|  06  | Gerente de Agência pode realizar alteração de dados dos seus clientes sem requisição (correção) |
|  07  | Comprovante de operações (correção) |
|  08  | Extrato de movimentação da conta (correção) |
<p align="center">
    <img src="docs/entregas/sprint-3/mvp-sprint3.gif">
</p>

### Sprint 4 
| Item | Funcionalidade             |
| :--: | :------------------------- |
|  01  | Configurações iniciais do sistema |
|  02  | Diferenciação entre tipos de conta Corrente e Poupança |
|  03  | Cheque Especial |
|  05  | Truncamento de valores |
|  06  | Responsividade do sistema |
<p align="center">
    <img src="docs/entregas/sprint-4/mvp-sprint4.gif">
</p>

<span id="tecnologias"></span>

## Tecnologias utilizadas
![Tecnologias utilizadas.](docs/imagens/tec-1.jpg "HTML5, CSS3, Python, Flask e MySQL.")

<span id="equipe"></span>

## Equipe
|    Função     | Nome                                |                     GitHub                   |
| :----------:  | :-----------------------            | :------------------------------------------: |
| Product Owner | Renan Souza Neves                   | [Github](https://github.com/Renan-Neves)     |
| Scrum Master  | Vinicius de Oliveira Laranjeiro     | [GitHub](https://github.com/noo-e)           |
|   Dev Team    | Bruno Denardo                       | [GitHub](https://github.com/brunodenardo)    |
|   Dev Team    | Matheus Fernando Vieira de Melo     | [GitHub](https://github.com/Matheusfvm)      |
|   Dev Team    | Murilo Henrique Sangi da Silva Lima | [GitHub](https://github.com/MuriloLima03)    |

