import requests
import telebot
import re

bot = telebot.TeleBot('8622319345:AAG_Gi4eemr3F7aznfIiKahBqiNPIVnb5ao')

usuarios = {}






# =========================
# START
# =========================
@bot.message_handler(commands=['start'])
def iniciar(msg):

    chat_id = msg.chat.id

    if chat_id not in usuarios:

        usuarios[chat_id] = {
            "temp": {}
        }

    bot.send_message(
        chat_id,
        'Olá!\n\nDigite o nome que deseja inserir:'
    )

    bot.register_next_step_handler(msg, receber_nome)


# =========================
# LISTAR USUÁRIOS
# =========================
@bot.message_handler(commands=['listar'])
def listar_usuarios(msg):

    chat_id = msg.chat.id

    response = requests.get(
        "https://meliz-control.onrender.com/user"
    )

    if response.status_code != 200:

        bot.send_message(
            chat_id,
            'Erro ao buscar usuários.'
        )

        return

    usuarios_api = response.json()

    if not usuarios_api:

        bot.send_message(
            chat_id,
            'Nenhum usuário cadastrado.'
        )

        return

    texto = '📋 USUÁRIOS CADASTRADOS\n\n'

    for usuario in usuarios_api:

        texto += (
            f'👤 Nome: {usuario["username"]}\n'
            f'📧 Email: {usuario["email"]}\n\n'
        )

    bot.send_message(chat_id, texto)


# =========================
# RECEBER NOME
# =========================
def receber_nome(msg):

    chat_id = msg.chat.id
    nome = msg.text.strip()

    usuarios[chat_id]["temp"]["nome"] = nome

    bot.send_message(
        chat_id,
        (
            f'Confirma este nome?\n\n'
            f'Nome: {nome}\n\n'
            'Digite: sim ou não'
        )
    )

    bot.register_next_step_handler(msg, confirmar_nome)


# =========================
# CONFIRMAR NOME
# =========================
def confirmar_nome(msg):

    chat_id = msg.chat.id
    resposta = msg.text.lower().strip()

    if resposta == 'sim':

        bot.send_message(
            chat_id,
            'Agora digite o email:'
        )

        bot.register_next_step_handler(msg, receber_email)

    elif resposta in ['não', 'nao']:

        bot.send_message(
            chat_id,
            'Digite o nome novamente:'
        )

        bot.register_next_step_handler(msg, receber_nome)

    else:

        bot.send_message(
            chat_id,
            'Resposta inválida.\nDigite apenas: sim ou não'
        )

        bot.register_next_step_handler(msg, confirmar_nome)


# =========================
# RECEBER EMAIL
# =========================
def receber_email(msg):

    chat_id = msg.chat.id
    email = msg.text.strip()

    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.fullmatch(padrao, email):

        bot.send_message(
            chat_id,
            'Email inválido.\nDigite novamente:'
        )

        bot.register_next_step_handler(msg, receber_email)
        return

    usuarios[chat_id]["temp"]["email"] = email

    bot.send_message(
        chat_id,
        (
            f'Confirma este email?\n\n'
            f'Email: {email}\n\n'
            'Digite: sim ou não'
        )
    )

    bot.register_next_step_handler(msg, confirmar_email)


# =========================
# CONFIRMAR EMAIL
# =========================
def confirmar_email(msg):

    chat_id = msg.chat.id
    resposta = msg.text.lower().strip()

    if resposta == 'sim':

        nome = usuarios[chat_id]["temp"]["nome"]
        email = usuarios[chat_id]["temp"]["email"]

        payload = {
            "username": nome,
            "email": email
        }

        response = requests.post(
            "http://127.0.0.1:5000/user/created",
            json=payload
        )

        if response.status_code == 201:

            bot.send_message(
                chat_id,
                (
                    'Usuário cadastrado com sucesso!\n\n'
                    f'Nome: {nome}\n'
                    f'Email: {email}\n\n'
                    'Deseja inserir outro?\n\n'
                    'Digite: sim ou não'
                )
            )

            bot.register_next_step_handler(msg, continuar_fluxo)

        else:

            bot.send_message(
                chat_id,
                'Erro ao salvar usuário.'
            )

    elif resposta in ['não', 'nao']:

        bot.send_message(
            chat_id,
            'Digite o email novamente:'
        )

        bot.register_next_step_handler(msg, receber_email)

    else:

        bot.send_message(
            chat_id,
            'Resposta inválida.\nDigite apenas: sim ou não'
        )

        bot.register_next_step_handler(msg, confirmar_email)


# =========================
# CONTINUAR FLUXO
# =========================
def continuar_fluxo(msg):

    chat_id = msg.chat.id
    resposta = msg.text.lower().strip()

    if resposta == 'sim':

        bot.send_message(
            chat_id,
            'Digite o próximo nome:'
        )

        bot.register_next_step_handler(msg, receber_nome)

    elif resposta in ['não', 'nao']:

        bot.send_message(
            chat_id,
            'Atendimento finalizado!'
        )

    else:

        bot.send_message(
            chat_id,
            'Resposta inválida.\nDigite apenas: sim ou não'
        )

        bot.register_next_step_handler(msg, continuar_fluxo)