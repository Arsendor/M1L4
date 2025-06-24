from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.first_ability = self.get_firstability()
        self.second_ability = self.get_secondability()

        self.level = 1          # уровень покемона
        self.satiety = 5        # сытость, максимум 10
        self.achievements = set()

        self.hp = randint(10,100)
        self.power = randint(1,30)

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    # Метод для получения названия 1-ой способности покемона через API
    def get_firstability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['abilities'][0]['ability']['name']
        else:
            return "overgrow"

    def get_secondability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            abilities = data['abilities']
            if len(abilities) > 1:
                return abilities[1]['ability']['name']
            else:
                return "Вторая способность отсутствует"
        else:
            return "unknown"

    def feed(self):
        if self.satiety < 10:
            self.satiety += 1
            message = f"{self.name} накормлен! Сытость: {self.satiety}/10."
            if self.satiety == 10:
                self.level_up()
                message += f" {self.name} достиг уровня {self.level}!"
            return message
        else:
            return f"{self.name} уже сытый!"

    def level_up(self):
        self.level += 1
        # Пример достижения на уровне 5
        if self.level == 5:
            self.achievements.add("Опытный тренер")
            print(f"{self.name} получил достижение 'Опытный тренер'!")


    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покемона: {self.name} , первая способность твоего покемона: {self.first_ability} , вторая способность твоего покемона: {self.second_ability} ."
        
    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img


