import telebot
from config import token
from logic import Pokemon, Wizard, Fighter
from random import randint
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        chance = randint(1,3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)

        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.get_img())
    else:
        bot.send_message(message.chat.id, "Ты уже создал себе покемона!")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        attacker_username = message.from_user.username
        target_username = message.reply_to_message.from_user.username

        if attacker_username in Pokemon.pokemons.keys() and target_username in Pokemon.pokemons.keys():
            attacker = Pokemon.pokemons[attacker_username]
            target = Pokemon.pokemons[target_username]

            result = attacker.attack(target)
            bot.send_message(message.chat.id, result)
            
            if target.hp == 0:
                bot.send_message(message.chat.id, f"{target.name} {target_username} был побежден!")
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами!")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщение того, кого хочешь атаковать!")


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

@bot.message_handler(commands=['heal'])
def heal_pok(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[username]
        heal_amount = randint(10, 30)
        result = pokemon.heal(heal_amount)
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, "У тебя еще нет покемона! Создай его с помощью команды /go.")


bot.infinity_polling(none_stop=True)
