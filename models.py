from db import BaseMeta
import ormar

# Exemplo de como criar um modelo:
# class Usuario(ormar.Model):
#     class Meta(BaseMeta):
#         tablename="tbl_usuario" 

class Shelter(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Abrigos"

    id:str = ormar.UUID(uuid_format= 'hex', primary_key=True)
    name:str = ormar.String(max_length=200)
    address:str = ormar.String(max_length=200)
    whats_app = ormar.String(max_length=200)
    lat = ormar.Decimal(precision=19, scale=0)
    lng = ormar.Decimal(precision=19, scale=0)
