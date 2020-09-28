import bot
import bot_exceptions as ex

if __name__ == '__main__':
    try:
        bot.Bot(
            token="",
            group_id=0
        ).start()
    except ex.AuthFail:
        print("Введены неверные данные для подключения!")
