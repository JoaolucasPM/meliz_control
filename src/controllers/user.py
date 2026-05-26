from flask import jsonify
from flask import Blueprint, request
from src.models.user import Product
from src.models.user import db
from src.views.user import UserSchema, CreatedeUserSchema
from marshmallow import ValidationError
from http import HTTPStatus



simple_user = Blueprint('user', __name__)
def create_user():

    user_schema = CreatedeUserSchema()

    try:
        data = user_schema.load(request.get_json())

    except ValidationError as exc:

        return {
            "errors": exc.messages
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    product = Product(
        produto=data["produto"],
        nome_cliente=data["nome_cliente"],
        valor_venda=data['valor_venda']
    )
    

    db.session.add(product)

    db.session.commit()

    return {
        "message": "Usuário criado!"
    }, HTTPStatus.CREATED

@simple_user.route("/user/created", methods=["POST"])
def created_user_BOT():
    
    data = request.get_json()
    
    product = Product(
        produto=data["produto"],
        nome_cliente=data["nome_cliente"],
        valor_venda=data['valor_venda']
        )

    db.session.add(product)

    db.session.commit()

    return {
        "message": "Usuário criado!"
    }, HTTPStatus.CREATED
    


def user_list():

    query = db.select(Product)

    users = db.session.execute(query).scalars().all()

    user_schema = UserSchema(many=True)

    return jsonify(user_schema.dump(users))
 
 
@simple_user.route("/user", methods=["POST", "GET"])
def user_create():

    if request.method == 'POST':
        return create_user()
    else:
        return user_list()
