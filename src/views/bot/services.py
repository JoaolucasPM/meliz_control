import requests



BASE_URL = "https://meliz-control.onrender.com"
#BASE_URL = "http://127.0.0.1:5000"


def listar_produtos():

    return requests.get(
        f"{BASE_URL}/user"
    )


def criar_usuario(payload):

    return requests.post(
        f"{BASE_URL}/user/created",
        json=payload
    )


