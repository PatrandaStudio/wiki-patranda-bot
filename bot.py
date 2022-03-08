import telebot
import config

from telebot import types

import wikipedia

bot = telebot.TeleBot(config.token)

wikipedia.set_lang("ru")

@bot.message_handler(content_types=['text'])
def text(message):
	global search_results
	search_results = wikipedia.search(message.text[0:50], results=5)
	if len(search_results) < 5:
		bot.send_message(message.chat.id, 'По данном запросу ничего не найденно')
	else:
		markup = types.InlineKeyboardMarkup()
		for i in range(0, 5):
			markup.add(types.InlineKeyboardButton(search_results[i], callback_data=str(i)))
		bot.send_message(message.chat.id, 'Вот что мне удалось найти по данному запросу', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	bot.send_message(call.message.chat.id, wikipedia.page(search_results[int(call.data)]).title + '\n' + wikipedia.summary(search_results[int(call.data)])[0:3500] + '...' + '\n' + wikipedia.page(search_results[int(call.data)]).url)

bot.infinity_polling()