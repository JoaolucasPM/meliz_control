from src.app import ma

from marshmallow import fields
from src.controllers.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        
class GetUser(ma.Schema):
    user_key = fields.Int(required=True, strict=True)  


class CreatedeUserSchema(ma.Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
