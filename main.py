import telebot
from config import token
from logic import Pokemon

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        pokemon = Pokemon(username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.get_img())
    else:
        bot.send_message(message.chat.id, "Ты уже создал себе покемона!")


@bot.message_handler(commands=['feed'])
def feed(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        response = pokemon.feed()
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Сначала создай покемона командой /go!")


@bot.message_handler(commands=['stats'])
def stats(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        bot.send_message(message.chat.id, pokemon.info2())
    else:
        bot.send_message(message.chat.id, "Сначала создай себе покемона с помощью команды /go!")

bot.infinity_polling(none_stop=True)