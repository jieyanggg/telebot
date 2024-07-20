import openai
import telebot
import requests
import os
from telebot import TeleBot, types
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEBOT_API_KEY = os.getenv("TELEBOT_API_KEY")


# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY 

bot = telebot.TeleBot(TELEBOT_API_KEY)

@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = f"Hello {message.from_user.first_name}!\n\nWelcome to the Chat GPT in Telegram. What is your question?"
    bot.send_message(chat_id=message.chat.id, text=welcome_message)

@bot.message_handler(commands=['quote'])
def send_quote(message):
    # Handler for the '/quote' command
    quote = get_random_quote()
    bot.reply_to(message, quote)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # Handler for all other messages
    response = generate_response(message.text)
    bot.reply_to(message, response)

def get_random_quote():
    # Fetch a random quote from an API
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = response.json()
        quote = data['content']
        author = data['author']
        return f"{quote}\n- {author}"
    return "Failed to fetch a quote. Please try again later"

def generate_response(prompt, model="gpt-4o"):
    # Generate an NLP response using the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message['content'].strip()


bot.infinity_polling()