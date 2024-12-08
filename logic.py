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
        self.hp = randint(50, 100) 
        self.power = randint(10, 30)
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
    
    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            shield_chance = randint(1,5)
            if shield_chance == 1:
                return "Покемон-волшебник применил щит в сражении"
            
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение {self.name} с {enemy.name}. У {enemy.name} осталось {enemy.hp} HP."
        else:
            enemy.hp = 0
            return f"Победа {self.name} над {enemy.name}!"
    
    def heal(self, amount):
        self.hp += amount
        return f"{self.name} восстановил {amount} HP. Текущее здоровье: {self.hp}."

    def info(self):
        rarity = "Редкий" if self.is_rare else "Обычный"
        return (
            f"Имя: {self.name}\n"
            f"Тип: {'Редкий' if self.is_rare else 'Обычный'}\n"
            f"Здоровье: {self.hp}\n"
            f"Сила: {self.power}\n"
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
    
class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power += randint(5, 15)  # Увеличиваем силу бойцу

    def info(self):
        return "У тебя покемон-боец!\n" + super().info()
    
    def attack(self, enemy):
        super_boost = randint(5,15)
        self.power += super_boost
        result = super().attack(enemy)
        self.power -= super_boost
        return result + f"\n{self.name} применил супер-атаку силой:{super_boost}"
    
    def gain_bonus(self):
        bonus = randint(5, 10)
        self.power += bonus
        return f"{self.name} получил бонус к силе: +{bonus}. Текущая сила: {self.power}."
class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp += randint(20, 30)  # Увеличиваем здоровье волшебнику

    def info(self):
        return "У тебя покемон-волшебник!\n" + super().info()

    def gain_bonus(self):
        bonus = randint(10, 20)
        self.hp += bonus
        return f"{self.name} получил бонус к здоровью: +{bonus}. Текущее здоровье: {self.hp}."
        
        
