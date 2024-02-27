import telebot
import csv
import logging
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '6690973653:AAG_TSqN89gVQBiHGLAm8KN7wjh9Y-D08B4'


logging.basicConfig(level=logging.INFO, encoding='utf-8',
                    format='%(asctime)s - %(funcName)s - %(message)s')


class Bot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.data = self.load_capitals()
        self.answer = None
        self.count = 0
        self.count_answer = 0

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == 'end':
                logging.debug('Запрос на завершение игры')
                self.bot.delete_message(call.message.chat.id, call.message.message_id)
                self.bot.send_message(call.message.chat.id, self.swow_results(), parse_mode='HTML')
                self.count = 0
                self.count_answer = 0
            else:
                if call.data == self.answer:
                    logging.info('Был дан верный ответ')
                    self.bot.answer_callback_query(call.id, 'Верно')
                    self.count += 1
                else:
                    logging.info("Был дан неверный ответ")
                    self.bot.answer_callback_query(call.id, 'Неверно')
                text, self.answer, options = self.get_question()
                keyboard = self.inline_keyboard(options)
                self.bot.edit_message_text(text, call.message.chat.id,
                                           call.message.message_id,
                                           reply_markup=keyboard, parse_mode='HTML')

        @self.bot.message_handler(commands=['start'])
        def start(message):
            logging.info('/start')
            text, self.answer, options = self.get_question()
            keyboard = self.inline_keyboard(options)
            self.bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=keyboard)


        @self.bot.message_handler(commands=['help'])
        def help(message):
            logging.info('/help')
            self.bot.send_message(message.chat.id, 'Отправьте /start чтобы начать',
                                                   parse_mode='HTML')

    def run(self):
        self.bot.infinity_polling()

    @staticmethod
    def inline_keyboard(options):
        logging.info('Создание inline клавиатуры')
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = [InlineKeyboardButton(s, callback_data=s) for s in options]
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton('Стоп игра', callback_data='end'))
        logging.info('inline клавиатура создана')
        return keyboard



    @staticmethod
    def load_capitals():
        capitals = dict()
        logging.info('Получение стран и столиц')
        try:
            with open('capitals.csv', newline='', encoding='utf-8') as f:
                data = csv.reader(f, delimiter=';')
                for line in data:
                    capitals[line[0]] = line[1]
        except Exception as e:
            logging.exception(e)
        logging.info('Список стран и столиц загружен')
        return capitals


    def get_question(self):
        logging.info('Получение вопроса')
        countries, capitals = list(self.data.keys()), list(self.data.values())
        random_countries = random.sample(countries, k=4)
        country = random.choice(random_countries)
        answer = self.data[country]
        options = [self.data[country] for country in random_countries]
        logging.info(f'Вопрос получен. Страна:{country} , столица:{answer} , варианты ответов:{options}')
        self.count_answer += 1
        return f'Назови столицу страны: <b>{country}</b>', answer, options


    def swow_results(self):
        logging.info('Результаты')
        text = f'Вы дали правильных ответов: {self.count} из {self.count_answer}'
        return text


if __name__ == '__main__':
    bot = Bot()
    bot.run()





