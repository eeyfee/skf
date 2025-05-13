
import telebot
import requests
import json

# Токен вашего бота (замените на свой)
TOKEN = '7825205587:AAE1OZE4PhxYYQqJPWfz7gmrdv7eTnDdryg'

bot = telebot.TeleBot(TOKEN)

# Список поддерживаемых валют в верхнем регистре
CURRENCIES = ['USD', 'EUR', 'RUB']

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        # Проверка поддержки валют
        valid_currencies = ['USD', 'EUR', 'RUB']
        if base not in valid_currencies:
            raise APIException(f"Валюта {base} не поддерживается.")
        if quote not in valid_currencies:
            raise APIException(f"Валюта {quote} не поддерживается.")

        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base}")
            if response.status_code != 200:
                raise APIException("Ошибка при обращении к API обменных курсов.")
            data = response.json()
            rates = data['rates']
            if quote not in rates:
                raise APIException(f"Курс для валюты {quote} недоступен.")
            rate = rates[quote]
            result = rate * float(amount)
            return result
        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка соединения с API: {e}")
        except json.JSONDecodeError:
            raise APIException("Ошибка обработки ответа от API.")

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