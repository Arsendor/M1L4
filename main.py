import telebot
import requests
from datetime import datetime, timedelta
from random import randint
from config import token

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.hp = 100
        self.last_feed_time = datetime.min

        # Выбираем случайного покемона из API (ID от 1 до 898)
        self.pokemon_id = randint(1, 898)
        api_url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            self.name = data['name'].capitalize()
            # Получаем спрайт покемона (главное изображение)
            self.img_url = data['sprites']['front_default']
        else:
            self.name = f"Pokemon#{self.pokemon_id}"
            self.img_url = None

        Pokemon.pokemons[pokemon_trainer] = self

    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            next_feed = self.last_feed_time + delta_time
            return f"Следующее время кормления покемона: {next_feed.strftime('%Y-%m-%d %H:%M:%S')}"

    def info(self):
        return f"Покемон {self.name}, здоровье: {self.hp}"

    def show_img(self):
        return self.img_url

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        pokemon = Pokemon(username)
        bot.send_message(message.chat.id, pokemon.info())
        if pokemon.img_url:
            bot.send_photo(message.chat.id, pokemon.show_img())
        else:
            bot.send_message(message.chat.id, "Изображение покемона недоступно.")
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['feed'])
def feed(message):
    username = message.from_user.username
    pokemon = Pokemon.pokemons.get(username)
    if not pokemon:
        bot.reply_to(message, "Сначала создай покемона командой /go")
        return
    reply = pokemon.feed()
    bot.send_message(message.chat.id, reply)

bot.infinity_polling(none_stop=True)