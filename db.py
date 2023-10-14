import databases
import ormar
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis de ambiente

db_driver = os.environ.get("DB_DRIVER")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")

# Coloque aqui a string de conexão com o banco de dados; 
# Deverá ter o seguinte formato: driver://user:pass@localhost/dbname
# Ref: https://learnbatta.com/blog/getting-started-with-alembic/
connection_string = f"{db_driver}://{db_user}:{db_pass}@{db_host}/{db_name}" 

database = databases.Database(connection_string)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


