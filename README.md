# Scaffolding - FastAPI + Alembic + Ormar + PostgreSQL

Estrutura base para aplicações web utilizando FastAPI, Alembic, Ormar e PostgreSQL.

# Comece por aqui

Bibliotecas, frameworks e etc. recebem atualizações constantemente, portanto verifique as versões das bibliotecas em `requirements.txt` para garantir que tudo esteja utilizando as versões mais recentes.
Esse projeto utiliza as seguintes dependências nas seguintes versões:
- [FastAPI](https://fastapi.tiangolo.com/) (0.103.2) -> https://pypi.org/project/fastapi/;
- [Uvicorn](https://www.uvicorn.org/) (0.23.2) -> https://pypi.org/project/uvicorn/;
- [Ormar](https://pypi.org/project/ormar/) (0.12.2) -> https://pypi.org/project/ormar/
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (1.12.0) -> https://pypi.org/project/alembic/
- [psycopg2-binary](https://www.psycopg.org/docs/install.html) (2.9.9) -> https://pypi.org/project/psycopg2-binary/
- [asyncpg](https://github.com/MagicStack/asyncpg) (0.28.0) -> https://pypi.org/project/asyncpg/

## Quero usar outro Sistema de Gerenciamento de Banco de Dados (SGBD)

Esse projeto foi configurado para utilizar PostgreSQL como banco de dados, mas fique a vontade para utilizar outro SGBD que mais lhe agradar. Faça o seguinte caso queira utilizar outro banco de dados:
- Remova as dependências `psycopg2-binary` e `asyncpg` de `requirements.txt`;
- Adicione as dependências do SGDB que você pretende utilizar.

## (opcional) - Criação do ambiente virtual

- Abra o terminal na pasta do projeto;
- Rode o comando `python3 -m venv .venv`. Será criado a pasta `.venv`;
- Utilize o comando `source .venv/bin/activate` para ativar o ambiente virtual.

## Instalando as dependências
- Acesse a pasta do projeto;
- Rode o comando: `pip install -r requirements.txt` ou `pip3 install -r requirements.txt`.

## Inicializando o alembic
- Rode o comando: `alembic init migrations` na pasta do projeto para inicializar o alembic;
- Será gerado o diretório `migrations` e o arquivo `alembic.ini`;

## Definido variáveis de ambiente
Para evitar deixar exposto variáveis relacionadas ao banco de dados, como: senha e usuário em nosso código, será utilizado um arquivo `.env` para definir esses valores sensíveis. Para isso, faça o seguinte:
- Crie um arquivo chamado `.env` na raiz do projeto;
- Acesse o arquivo `.env-template`, copie o conteúdo e cole no arquivo `.env`;
- Depois de colar, defina os valores das variáveis de ambiente. Você irá definir o seu nome de usuário, senha e o nome da sua base de dados. **DB_DRIVER você só precisa alterar caso queira usar outro SGDB**. Exemplo:
```
DB_DRIVER="postgresql"
DB_USER="christian"
DB_PASS="christian123"
DB_HOST="localhost"
DB_NAME="db_fastapi_alembic"
```
### Um rápido aviso
As variáveis de ambiente são utilizadas no arquivo `alembic.ini`, se sua senha possuir caracteres especiais, como: @, $, % etc. pode ser que ocorra um erro de interpolação. Ainda não descobri o porquê que isso ocorre, mas parece que o alembic não consegue tratar muito bem esses caracteres e levanta essa exceção. Abaixo eu coloquei um link de um post no StackOverflow sobre o problema. A solução proposta não funcionou com senhas que possuem `@`, mas pode ser que funcione com outros caracteres especiais.
https://stackoverflow.com/questions/73892869/python-3-10-6-alembic-postgresql-password-with-special-character

## Onde as variáveis de ambiente são utilizadas?
As variáveis de ambiente são utilizadas nos seguintes arquivos:
- `alembic.ini` -> Na linha 65 (sqlalchemy.url) as variáveis de ambiente são utilizadas para montar a string de conexão que será utilizada pelo alembic.
- `db.py` -> Nesse arquivo as variáveis de ambiente são utilizadas para montar a connection string a ser utilizada pelo Ormar.

## Utilizando outro SGDB
Conforme foi dito em **Definido variáveis de ambiente** "[...] DB_DRIVER você só precisa alterar caso queira usar outro SGDB". Portanto, caso queira utilizar outro SGDB, além de adicionar as dependências necessárias, você precisará acessar o arquivo `.env` e alterar o valor de DB_DRIVER para o banco de dados que você deseja utilizar.

# Migrations (Migrações)

## Criando um modelo
Você pode criar seus modelos em models.py, mas sinta-se a vontade para criar outro arquivo para criar as suas classes. Porém, é importante que seu modelo tenha a seguinte estrututra:
```
from db import BaseMeta 
import ormar

class MeuModelo(ormar.Model):
    class Meta(BaseMeta):
        tablename="NOME_DA_TABELA"

    # coloque aqui seus atributos e métodos.
```
- `class MeuModelo(ormar.Model)` -> Estamos fazendo nosso modelo herdar de ormar.Model para que tenhamos os métodos de busca, inserção, atualização, deleção e remoção que o Ormar nos proporciona;
- `class Meta(BaseMeta)` -> Em `BaseMeta` nós definimos as configurações do banco de dados e aqui, através da herança, estamos passando essas configurações para o Ormar.

## Automatizando as migrações
Para que as migrations sejam geradas automaticamente é preciso fazer o seguinte:
- Acesse o arquivo `env.py` (`migrations/env.py`);
- Cole o seguinte código para carregar as variáveis de ambiente:
```
section = config.config_ini_section

config.set_section_option(section, "DB_USER", os.environ.get("DB_USER"))
config.set_section_option(section, "DB_PASS", os.environ.get("DB_PASS"))
config.set_section_option(section, "DB_HOST", os.environ.get("DB_HOST"))
config.set_section_option(section, "DB_NAME", os.environ.get("DB_NAME"))
```
- Importe seu modelo `from models import MeuModelo`;
- Abaixo do importe do seu modelo, realize o importe de: `from db import BaseMeta`;
- Procure por `target_metadata` e faça o seguinte: `target_metadata = BaseMeta.metadata`;
- Importante: Todo modelo que você criar, você deverá importa-lo no arquivo `env.py` (`migrations/env.py`)

## Comandos

- **Gerando arquivo de migração:** `alembic revision --autogenerate -m "DESCRIÇÃO_DA_MIGRATION"` -> Gera o arquivo de migração. Substitua DESCRIÇÃO_DA_MIGRATION por algo que descreva a migração que você está realizando. Exemplo: `alembic revision --autogenerate -m "Criando tabela usuário"`.
- **Visualizando o SQL gerado pela migration**: `alembic upgrade head --sql` -> Permite visualizar o script SQL que será utilizado quando sua migração for aplicada;
- **Aplicando a migração**: `alembic upgrade head` -> Aplica as migrações no banco de dados.
- **Defazendo a última migração**: `alembic downgrade -1` -> Desfaz a última migração.

# Rodando a aplicação
- Abra o terminal e rode o comando: `uvicorn main:app --reload`

# Referências

https://hackernoon.com/how-to-set-up-fastapi-ormar-and-alembic

https://learnbatta.com/blog/getting-started-with-alembic/


