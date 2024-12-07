from random import randint, random
import requests
import time
class Pokemon:
    pokemons = {}
    last_fed = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.abilities = self.get_abilities()
        self.level = 1
        self.experience = 0
        self.is_rare = self.check_if_rare()
        Pokemon.pokemons[pokemon_trainer] = self
        Pokemon.last_fed[pokemon_trainer] = 0

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        return "Pikachu"

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['other']['official-artwork']['front_default']
        return None

    def get_abilities(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['abilities'][0]['ability']['name'])
        return ["Unknown"]

    def check_if_rare(self):
        return random() < 0.1

    def feed(self):
        self.experience += 5
        if self.experience >= self.level * 10:
            self.level_up()
    
    def feed(self):
        current_time = time.time()
        last_fed_time = Pokemon.last_fed[self.pokemon_trainer]
        if current_time - last_fed_time < 30:
            remaining_time = int(30 - (current_time - last_fed_time))
            return f"У {self.name} полон живот! Подожди {remaining_time} секунд."
        else:
            Pokemon.last_fed[self.pokemon_trainer] = current_time
            self.experience += 5
            level_up_message = self.check_level_up()
            return f"{self.name} был покормлен! Получено 5 опыта.\n{level_up_message}"

    def check_level_up(self):
        if self.experience >= self.level * 10:
            self.level += 1
            return f"Уровень повышен! Теперь уровень: {self.level}"
        return ""

    def info(self):
        rarity = "Редкий" if self.is_rare else "Обычный"
        return (
            f"Имя: {self.name}\n"
            f"Тип: {'Редкий' if self.is_rare else 'Обычный'}\n"
            f"Способности: {self.abilities}"
        )
    
    def info2(self):
        rarity = "Редкий" if self.is_rare else "Обычный"
        return (
            f"Имя: {self.name}\n"
            f"Тип: {'Редкий' if self.is_rare else 'Обычный'}\n"
            f"Уровень: {self.level}\n"
            f"Опыт: {self.experience}\n"
            f"Способности: {self.abilities}"
        )
