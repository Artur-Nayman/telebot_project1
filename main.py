import telebot
from telebot import types

bot = telebot.TeleBot('6258928093:AAHhXtkLv-gnU82zkaA43j7QrvhoshU8olk')

# StartBot with buttons
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    project = types.KeyboardButton("Project")
    cv = types.KeyboardButton("CV")
    hub = types.KeyboardButton("GitHub")
    linked = types.KeyboardButton("LinkedIn")
    markup.add(project, cv, hub, linked)
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}!", reply_markup=markup)

# Speak and answer
@bot.message_handler()
def get_user_text(message):
    greetings = ["Hello", "Hi", "hello", "hi", "Good morning", "good morning", "Good afternoon", "Good evening", "Greetings", "Howdy", "good afternoon", "good evening", "greetings", "howdy"]
    tynks = ["ty", "Thank you" "Thanks", "Ty", "thank you", "thanks"]
    if any(greeting in message.text for greeting in greetings):
        bot.send_message(message.chat.id, "How can i help you? \n\nYou can look at the list of buttons at the bottom right to select one of the available options", parse_mode="html")
    elif any(tynks in message.text for tynks in tynks):
        bot.send_message(message.chat.id, "Always at your service", parse_mode="html")
    elif message.text == "Project":
        # URL send
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Website Project", url="albatrosry.com"))
        markup.add(types.InlineKeyboardButton("My Page", url="https://albatrosry.com/?page_id=1257&lang=fi"))
        bot.send_message(message.chat.id, "Here is the site that I created.\nNow there is a new administrator, who deleted half of features what i added :( \nBut on \"My Page\" you can see proofs about that i been andministrator of that website.", reply_markup=markup)
    elif message.text == "CV":
        #CV send
        markup = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, "Here is my CV", reply_markup=markup)
        # File send
        chat_id = message.chat.id
        document_path = 'CV.pdf'
        with open(document_path, 'rb') as document:
            bot.send_document(chat_id, document)
    elif message.text == "GitHub":
        # URL send
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("To GitHub", url="https://github.com/Artur-Nayman"))
        bot.send_message(message.chat.id, "Here is my GitHub", reply_markup=markup)
    elif message.text == "LinkedIn":
        # URL send
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Linkedin", url="https://www.linkedin.com/in/artur-nayman-98ba12200/"))
        bot.send_message(message.chat.id, "Here is my LinkedIn", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "I'm sorry, I didn't understand the command")

# none stop working
bot.polling(none_stop=True)
