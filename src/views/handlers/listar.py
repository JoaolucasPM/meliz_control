from src.views.bot.main import bot

from src.views.bot.services import listar_produtos


@bot.message_handler(commands=['listar'])
def listar(msg):

    chat_id = msg.chat.id

    response = listar_produtos()

    if response.status_code != 200:

        bot.send_message(
            chat_id,
            'Erro ao buscar usuários.'
        )

        return

    produtos = response.json()

    if not produtos:

        bot.send_message(
            chat_id,
            'Nenhum produto cadastrado.'
        )

        return

    texto = '📋 Relatorio de produtos\n\n'

    for produto in produtos:

        texto += (
            f'👤 Cliente: {produto["nome_cliente"]}\n'
            f'📧 Produto: {produto["produto"]}\n'
            f'📧 Valor: (R$): {produto["valor_venda"]}\n\n'
        )

    bot.send_message(chat_id, texto)