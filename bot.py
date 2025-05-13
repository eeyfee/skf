# bot.py
import telebot
import config
from extensions import APIException
from extensions import CryptoConverter
# import config


bot = telebot.TeleBot(config.TOKEN)

CURRENCIES = ['USD', 'EUR', 'RUB']


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот-конвертер валют.\n"
        "Чтобы выполнить конвертацию, введите сообщение в формате:\n"
        "<валюта_источник> <валюта_цель> <количество>\n"
        "Например:\nUSD EUR 100"
    )

@bot.message_handler(content_types=['text'])
def handle_message(message):
    try:
        parts = message.text.strip().split()
        if len(parts) != 3:
            raise APIException("Неверный формат ввода. Используйте: <валюта_источник> <валюта_цель> <количество>.")

        base_currency, quote_currency, amount_str = parts

        # Проверка поддержки валют
        if base_currency not in CURRENCIES:
            raise APIException(f"Валюта {base_currency} не поддерживается.")
        if quote_currency not in CURRENCIES:
            raise APIException(f"Валюта {quote_currency} не поддерживается.")

        # Проверка количества
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            raise APIException("Количество должно быть положительным числом.")

        # Получение курса и расчет
        price = CryptoConverter.get_price(base_currency, quote_currency, amount)
        reply_text = f"{amount} {base_currency} равно примерно {price:.2f} {quote_currency}"
        bot.send_message(message.chat.id, reply_text)

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла непредвиденная ошибка: {e}")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)



