from flask import Blueprint, request
from src.models.user import User
from src.models.user import db
from src.views.user import UserSchema, CreatedeUserSchema
from marshmallow import ValidationError
from http import HTTPStatus



simple_user = Blueprint('user', __name__)



from http import HTTPStatus

from flask import request
from marshmallow import ValidationError

from src.models.base import db
from src.models.user import User
from src.views.user import CreatedeUserSchema


def create_user():

    user_schema = CreatedeUserSchema()

    try:
        data = user_schema.load(request.get_json())

    except ValidationError as exc:

        return {
            "errors": exc.messages
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(
        username=data["username"],
        email=data["email"]
    )

    db.session.add(user)

    db.session.commit()

    return {
        "message": "Usuário criado!"
    }, HTTPStatus.CREATED

def user_list():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)

@simple_user.route("/user", methods=["POST", "GET"])
def user_create():

    if request.method == 'POST':
        return create_user()
    else:
        return user_list()
