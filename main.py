import telebot
from telebot import types

bot = telebot.TeleBot('6258928093:AAHhXtkLv-gnU82zkaA43j7QrvhoshU8olk')

# StartBot with buttons
@bot.message_handler(commands=["start", "help"])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    project = types.KeyboardButton("Project")
    cv = types.KeyboardButton("CV")
    markup.add(project, cv)
    bot.send_message(message.chat.id, "Приветсвую вас", reply_markup=markup)

# Speak and answer
@bot.message_handler()
def get_user_text(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, "Чем могу помочь?", parse_mode="html")
    elif message.text == "id":
        bot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}", parse_mode="html")
    elif message.text == "Спасибо":
        bot.send_message(message.chat.id, "Всегда к вашим услугам", parse_mode="html")
    elif message.text == "Project":
        # URL send
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Website Project", url="albatrosry.com"))
        bot.send_message(message.chat.id, "Here is the site that I created.\nNow there is a new administrator, who deleted half of features what i added :(.", reply_markup=markup)
    elif message.text == "CV":
        #CV send
        markup = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, "Here is my CV", reply_markup=markup)
        # File send
        chat_id = message.chat.id
        document_path = 'CV.pdf'
        with open(document_path, 'rb') as document:
            bot.send_document(chat_id, document)
    else:
        bot.send_message(message.chat.id, "Прошу прощения, я не понял команду")

# none stop working
bot.polling(none_stop=True)
