import telebot
import mysql.connector
from telebot import types
from bs4 import BeautifulSoup as BS
from requests import get

#З'єднання з базою даних
#connect to database
conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="root", database="artur_bot")
cursor = conn.cursor()
#Parsed web page url
url = "https://www.eneba.com/store/xbox-game-pass?drms[]=xbox&page=1&regions[]=emea&regions[]=europe&regions[]=finland&regions[]=global&text=game%20pass%20subscription&types[]=subscription"
#key to telegram chat
bot = telebot.TeleBot('6258928093:AAERQF1wZjvEaDTBeTlVQPGAQFC_lk1KADw')
r = get(url)
site = BS(r.text, 'html.parser')
#Getting name and price from "span" in they clear form
not_clear_game = site.find_all('span', class_="YLosEL")
not_clear_price = site.find_all('span', class_="L5ErLT")
game = [c.text for c in not_clear_game]
game_price =[c.text for c in not_clear_price]
price = [float(price[1:]) for price in game_price] #Превращает в флоат каждый элемент списка не считая превый | Transformation into float every element instead first
filter_price = 0
n_game = []



def prices():
    #Getting all needed values and puting them into database
    global n_game
    global game
    try:
        delete_query = "DELETE FROM xbox"
        cursor.execute(delete_query)
        count = -1
        while count != game:
            count = count + 1
            if price[count] > filter_price:
                continue
            Title = game[count]
            Price = price[count]
            n_game.append(game[count])
            n_game.append(price[count])
            sql = "INSERT INTO xbox (Title, Price) VALUES (%s, %s)"
            cursor.execute(sql, (Title, Price))
            conn.commit()
        # Закрытие курсора и соединения с базой данных | Closing the cursor and connecting to the database
        cursor.close()
        conn.close()
    except:
        None

@bot.message_handler(commands=["start"])# Починає бота з кнопками | Starting bot + show buttons
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    project = types.KeyboardButton("Project")
    cv = types.KeyboardButton("CV")
    hub = types.KeyboardButton("GitHub")
    linked = types.KeyboardButton("LinkedIn")
    markup.add(project, cv, hub, linked)
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}!", reply_markup=markup)

@bot.message_handler(func=lambda message: True) #Xbox message and others in same handler
def handle_message(message):
    global filter_price
    global n_game
    global game
    #Вивід списку Xbox
    #Xbox list output
    try:
        filter_price = float(message.text)  # Преобразование введенного значения в число | Conversion of the entered value into a number
        prices()
        # Выполнение SQL-запроса для выборки данных
        # Exrcution of SQL-query for data selection
        sql = "SELECT Title, Price FROM xbox"
        cursor.execute(sql)
        # Получение результатов запроса
        # Receiving request results
        results = cursor.fetchall()
        # Вывод данных
        # Data output
        for row in results:
            title = row[0]# Получение названия игры из первого столбца (индекс 0) | Get name of game (index 0)
            price = row[1] # Получение цены игры из второго столбца (индекс 1) | Get price of game (index 1)
            bot.reply_to(message, f'Title: {title} \n \nPrice: {price}$') #Send answer


        return
    except ValueError:
        None
    #List of words on which bot gonna react
    greetings = ["Hello", "Hi", "hello", "hi", "Good morning", "good morning", "Good afternoon", "Good evening", "Greetings", "Howdy", "good afternoon", "good evening", "greetings", "howdy"]
    tynks = ["ty", "Thank you", "Thanks", "Ty", "thank you", "thanks"]
    #react to greetings
    if any(greeting in message.text for greeting in greetings):
        bot.send_message(message.chat.id, "How can i help you? \n\nYou can look at the list of buttons at the bottom right to select one of the available options", parse_mode="html")
    #react to tynks
    elif any(tynks in message.text for tynks in tynks):
        bot.send_message(message.chat.id, "Always at your service", parse_mode="html")
    #Button for my project(in future gonna be portfolio
    elif message.text == "Project":
        # URL send
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("First Project", url="albatrosry.com"))
        markup.add(types.InlineKeyboardButton("My Page", url="https://albatrosry.com/?page_id=1257&lang=fi"))
        markup.add(types.InlineKeyboardButton("Second Project", url="https://artur-nayman.github.io/Asiakasty-2022v2/"))
        bot.send_message(message.chat.id, "Here is the sites that I created.\nNow in the first is a new administrator, who deleted half of features what i added :( \nBut on \"My Page\" you can see proofs about that i been andministrator of that website.\nIn second project you can see original web site created when i was project manager. \nNew projects you can see on my GitHub.", reply_markup=markup)
    #Button for my CV
    elif message.text == "CV":
        #CV send
        markup = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, "Here is my CV", reply_markup=markup)
        # File send
        chat_id = message.chat.id
        document_path = 'CV.pdf'
        with open(document_path, 'rb') as document:
            bot.send_document(chat_id, document)
    #Button for my GitHub
    elif message.text == "GitHub":
        # URL send
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("To GitHub", url="https://github.com/Artur-Nayman"))
        bot.send_message(message.chat.id, "Here is my GitHub", reply_markup=markup)
    #Button for my LinkedIn
    elif message.text == "LinkedIn":
        # URL send
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Linkedin", url="https://www.linkedin.com/in/artur-nayman-98ba12200/"))
        bot.send_message(message.chat.id, "Here is my LinkedIn", reply_markup=markup)

# none stop working
bot.polling(none_stop=True)
