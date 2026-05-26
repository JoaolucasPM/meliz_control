from src.views.bot.main import bot

from src.views.bot.states import usuarios

from src.views.bot.services import criar_usuario


# =========================
# RECEBER NOME CLIENTE
# =========================
def receber_nome_cliente(msg):

    chat_id = msg.chat.id

    nome_cliente = msg.text.strip()

    usuarios[chat_id]["temp"]["nome_cliente"] = nome_cliente

    bot.send_message(
        chat_id,
        (
            f'Confirma este cliente?\n\n'
            f'Cliente: {nome_cliente}\n\n'
            'Digite: sim ou não'
        )
    )

    bot.register_next_step_handler(
        msg,
        confirmar_nome_cliente
    )


# =========================
# CONFIRMAR NOME CLIENTE
# =========================
def confirmar_nome_cliente(msg):

    chat_id = msg.chat.id

    resposta = msg.text.lower().strip()

    if resposta == 'sim':

        bot.send_message(
            chat_id,
            'Digite o produto:'
        )

        bot.register_next_step_handler(
            msg,
            receber_produto
        )

    elif resposta in ['não', 'nao']:

        bot.send_message(
            chat_id,
            'Digite o nome novamente:'
        )

        bot.register_next_step_handler(
            msg,
            receber_nome_cliente
        )

    else:

        bot.send_message(
            chat_id,
            'Digite apenas: sim ou não'
        )

        bot.register_next_step_handler(
            msg,
            confirmar_nome_cliente
        )


# =========================
# RECEBER PRODUTO
# =========================
def receber_produto(msg):

    chat_id = msg.chat.id

    produto = msg.text.strip()

    usuarios[chat_id]["temp"]["produto"] = produto

    bot.send_message(
        chat_id,
        (
            f'Confirma este produto?\n\n'
            f'Produto: {produto}\n\n'
            'Digite: sim ou não'
        )
    )

    bot.register_next_step_handler(
        msg,
        confirmar_produto
    )


# =========================
# CONFIRMAR PRODUTO
# =========================
def confirmar_produto(msg):

    chat_id = msg.chat.id

    resposta = msg.text.lower().strip()

    if resposta == 'sim':

        bot.send_message(
            chat_id,
            'Digite o valor da venda:'
        )

        bot.register_next_step_handler(
            msg,
            receber_valor
        )

    elif resposta in ['não', 'nao']:

        bot.send_message(
            chat_id,
            'Digite o produto novamente:'
        )

        bot.register_next_step_handler(
            msg,
            receber_produto
        )

    else:

        bot.send_message(
            chat_id,
            'Digite apenas: sim ou não'
        )

        bot.register_next_step_handler(
            msg,
            confirmar_produto
        )


# =========================
# RECEBER VALOR
# =========================
def receber_valor(msg):

    chat_id = msg.chat.id

    valor = msg.text.strip()

    try:

        valor = float(valor.replace(',', '.'))

    except ValueError:

        bot.send_message(
            chat_id,
            'Valor inválido.\nDigite novamente:'
        )

        bot.register_next_step_handler(
            msg,
            receber_valor
        )

        return

    usuarios[chat_id]["temp"]["valor_venda"] = valor

    bot.send_message(
        chat_id,
        (
            f'Confirma este valor?\n\n'
            f'Valor: R$ {valor:.2f}\n\n'
            'Digite: sim ou não'
        )
    )

    bot.register_next_step_handler(
        msg,
        confirmar_valor
    )


# =========================
# CONFIRMAR VALOR
# =========================
def confirmar_valor(msg):

    chat_id = msg.chat.id

    resposta = msg.text.lower().strip()

    if resposta == 'sim':

        payload = {
            "nome_cliente": usuarios[chat_id]["temp"]["nome_cliente"],
            "produto": usuarios[chat_id]["temp"]["produto"],
            "valor_venda": usuarios[chat_id]["temp"]["valor_venda"]
        }

        response = criar_usuario(payload)

        if response.status_code == 201:

            bot.send_message(
                chat_id,
                (
                    'Venda cadastrada com sucesso!\n\n'
                    'Deseja inserir outra?\n\n'
                    'Digite: sim ou não'
                )
            )

            bot.register_next_step_handler(
                msg,
                continuar_fluxo
            )

        else:

            bot.send_message(
                chat_id,
                'Erro ao salvar venda.'
            )

    elif resposta in ['não', 'nao']:

        bot.send_message(
            chat_id,
            'Digite o valor novamente:'
        )

        bot.register_next_step_handler(
            msg,
            receber_valor
        )

    else:

        bot.send_message(
            chat_id,
            'Digite apenas: sim ou não'
        )

        bot.register_next_step_handler(
            msg,
            confirmar_valor
        )


# =========================
# CONTINUAR FLUXO
# =========================
def continuar_fluxo(msg):

    chat_id = msg.chat.id

    resposta = msg.text.lower().strip()

    if resposta == 'sim':

        bot.send_message(
            chat_id,
            'Digite o nome do cliente:'
        )

        bot.register_next_step_handler(
            msg,
            receber_nome_cliente
        )

    elif resposta in ['não', 'nao']:

        bot.send_message(
            chat_id,
            'Atendimento finalizado!'
        )

    else:

        bot.send_message(
            chat_id,
            'Digite apenas: sim ou não'
        )

        bot.register_next_step_handler(
            msg,
            continuar_fluxo
        )