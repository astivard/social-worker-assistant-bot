from telebot import TeleBot, types

from auth_data import token
from script import get_total
from days_month_data import correct_week_day_names


def main(token):
    bot = TeleBot(token)

    week_days = []
    is_privileged = False

    def show_keypad_1():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('ДА')
        btn2 = types.KeyboardButton('НЕТ')
        markup.add(btn1, btn2)
        return markup

    def show_keypad_2():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        btn1 = types.KeyboardButton('ПН')
        btn2 = types.KeyboardButton('ВТ')
        btn3 = types.KeyboardButton('СР')
        btn4 = types.KeyboardButton('ЧТ')
        btn5 = types.KeyboardButton('ПТ')
        btn6 = types.KeyboardButton('Рассчитать')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        return markup

    def add_week_day(message: str):
        if message in week_days:
            pass
        else:
            week_days.append(message)

    def sort_week(week_days) -> list:
        days_numbers = sorted([correct_week_day_names[item] for item in week_days])
        correct_week = [list(correct_week_day_names.keys())[week_day_number] for week_day_number in days_numbers]
        return correct_week

    def get_result_message() -> str:
        total, number_of_visit_days, coef, month = get_total(is_privileged, week_days)
        result_message = f"Вы посетили пожилого в <b>{month} {number_of_visit_days}</b> дней.\n\n" \
                         f"Сумма:     <code>{number_of_visit_days} * {coef} = {total}</code>     рублей."
        return result_message

    @bot.message_handler(commands=["start"])
    def start(message):
        nonlocal week_days
        week_days.clear()
        start_message = f"Здравствуйте, <b>{message.from_user.first_name}</b>!👋🏻\n" \
                        f"\nЭтот бот поможет вам рассчитать сумму за месяц по обслуживаемому пожилому."
        bot.send_message(message.chat.id, start_message, parse_mode="html")

        bot.send_message(message.chat.id, "Выберите, является ли пожилой льготником: 👇🏻",
                         reply_markup=show_keypad_1())

    @bot.message_handler(content_types=['text'])
    def mess(message):
        get_message_bot = message.text.strip()
        nonlocal is_privileged, week_days

        if get_message_bot == "ДА":
            is_privileged = True
            week_days.clear()
            bot.send_message(message.chat.id, "Выберите дни недели, в которые он обслуживается: 👇🏻",
                             reply_markup=show_keypad_2())

        elif get_message_bot == "НЕТ":
            is_privileged = False
            week_days.clear()
            bot.send_message(message.chat.id, "Выберите дни недели, в которые он обслуживается: 👇🏻",
                             reply_markup=show_keypad_2())

        elif get_message_bot in ('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ'):
            add_week_day(get_message_bot)

            week_message = f"Вы выбрали дни недели:\n<b>{' '.join(sort_week(week_days))}</b>"
            bot.send_message(message.chat.id, week_message, parse_mode="html")

        elif get_message_bot == "Рассчитать":
            result_message = get_result_message()
            week_days.clear()
            bot.send_message(message.chat.id, result_message, parse_mode="html")
            bot.send_message(message.chat.id, "Выберите, является ли пожилой льготником: 👇🏻",
                             reply_markup=show_keypad_1())
        else:
            print(get_message_bot)

    bot.infinity_polling()


if __name__ == "__main__":
    main(token)
