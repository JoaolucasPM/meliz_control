from src.views.bot.main import bot

from src.views.bot.states import usuarios

from src.views.handlers.cadastro import receber_nome_cliente


@bot.message_handler(commands=['start'])
def iniciar(msg):

    chat_id = msg.chat.id

    if chat_id not in usuarios:

        usuarios[chat_id] = {
            "temp": {}
        }

    bot.send_message(
        chat_id,
        'Olá!\n\nDigite o nome do cliente:'
    )

    bot.register_next_step_handler(
        msg,
        receber_nome_cliente
    )