import os
import telebot
import json


from database.queries import get_messages, save_message, initiate_database, is_user_admin, make_admin, create_user, see_users, reset_database, see_messages
from openai import OpenAI
from dotenv import load_dotenv
from botAI.botAI import generate_content
from botAI.prompts import system_prompt

def create_msg(role, content):
    return {
        "role": role,
        "content": content,
    }

def format_message(role, content):
    return json.dumps(create_msg(role, content))

load_dotenv()
openrouter_API = os.environ.get("OPENROUTER_KEY")
bot_API = os.environ.get("BOT_API")
database_name = os.environ.get("DATABASE_NAME")
password = os.environ.get("PASSWORD")

initiate_database(database_name)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_API,
)


bot = telebot.TeleBot(bot_API)
print("the bot is running! Check it on t.me/ai_traininggrounds_bot")

@bot.message_handler(commands=['see_users'])
def base(message):
    print(see_users(database_name))
    bot.send_message(message.chat.id, "ok")

@bot.message_handler(commands=["start"])
def start(message):
    try:
        if len(get_messages(database_name, message)) < 1:
            create_user(database_name, message)
    except Exception as e:
        print(e)
    finally:
        bot.send_message(message.chat.id, "Glad to meet you!")


@bot.message_handler(commands=["admin"])
def check_admin(message):
    # print(is_user_admin(database_name, message))
    if len(message.text.split()) == 2:
        
        if message.text.split()[1] == password:
            make_admin(database_name, message)
            bot.send_message(message.chat.id, "You've been promoted to admin!")
        else:
            bot.send_message(message.chat.id, "nope!")
    else:
        check = is_user_admin(database_name, message)
        
        if len(check) == 0:
            create_user(database_name, message)
            bot.send_message(message.chat.id, "We just met!")
            return
        
        if check[0][1] != 0:
            bot.send_message(message.chat.id, "alright!")
        else:
            
            bot.send_message(message.chat.id, "nope!")
    

@bot.message_handler(commands=["reset"])
def reset_db(message):
    check = is_user_admin(database_name, message)
    if len(check) != 0 and check[0][1] == 1:
        reset_database(database_name)
        print(see_messages(database_name))
        bot.send_message(message.chat.id, "The database has been reset")


@bot.message_handler(commands=["help"])
def help_func(message):
    try:
        if len(get_messages(database_name, message)) < 1:
            create_user(database_name, message)
    except Exception as e:
        print(e)
    finally:
        # bot.send_message(message.chat.id, "Glad to meet you!")
        bot.send_message(message.chat.id, "no help here")



@bot.message_handler(content_types=['text'])
def reply_func(message):
    messages = []
    if len(get_messages(database_name, message)) < 1:
        try:
            create_user(database_name, message)
        except Exception as e:
            print(e)
        messages.append(create_msg("system", system_prompt))
        msg_text = json.dumps(messages[0])
        save_message(database_name, message, msg_text)
    else:
        messagesJSON = get_messages(database_name, message)
        for msg in messagesJSON:
            messages.append(json.loads(msg))

    messages.append(create_msg("user", message.text))
   
    msg_text = format_message("user", message.text)
    save_message(database_name, message, msg_text)

    response = generate_content(client, messages)
    messages.append(create_msg("assistant", response))

    save_message(database_name, message, format_message("assistant", response))
    bot.send_message(message.chat.id, response)


bot.infinity_polling()

