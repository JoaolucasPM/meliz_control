from threading import Thread

from src.app import create_app

from src.views.bot.main import bot


import src.views.handlers.start
import src.views.handlers.listar
import src.views.handlers.cadastro

app = create_app()


def iniciar_bot():

    print('BOT INICIADO')

    bot.infinity_polling(
        skip_pending=True
    )


bot_thread = Thread(
    target=iniciar_bot
)

bot_thread.daemon = True

bot_thread.start()


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000,
        use_reloader=False
    )