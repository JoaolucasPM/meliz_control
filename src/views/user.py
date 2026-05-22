from src.app import ma

from marshmallow import fields
from src.controllers.user import Product

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        
class GetUser(ma.Schema):
    user_key = fields.Int(required=True, strict=True)  


class CreatedeUserSchema(ma.Schema):
    produto = fields.String(required=True)
    cliente = fields.String(required=True)
    valor_venda = fields.String(required=True)


