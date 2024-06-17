# warrior.py
from character import Character

class Warrior(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Warrior", armor=10, max_hp=max_hp)
        self.__max_stamina = 100
        self.__current_stamina = self.__max_stamina
        self.__stamina_regeneration = 10
        self.__strength = 15
        self.__attacks = {
            "Basic Attack": {"method": self.basic_attack, "stamina_cost": 10},
            "Charge": {"method": self.charge, "stamina_cost": 20},
            "Cleave Attack": {"method": self.cleave_attack, "stamina_cost": 30},
            "Shield Bash": {"method": self.shield_bash, "stamina_cost": 15},
            "Defensive Stance": {"method": self.defensive_stance, "stamina_cost": 5},
        }

    def basic_attack(self, target):
        damage = self.__strength
        print(f"{self.get_name()} performs a basic attack on {target.get_name()} for {damage} damage!")
        target.take_damage(damage)

    def charge(self, target):
        print(f"{self.get_name()} charges towards {target.get_name()}!")
        target.take_damage(self.__strength)

    def cleave_attack(self, targets):
        for target in targets:
            damage = self.__strength * 2
            print(f"{self.get_name()} cleaves {target.get_name()} for {damage} damage!")
            target.take_damage(damage)

    def shield_bash(self, target):
        damage = self.__strength + 5
        print(f"{self.get_name()} performs a shield bash on {target.get_name()} for {damage} damage!")
        target.take_damage(damage)

    def defensive_stance(self):
        self.set_armor_class(self.get_armor_class() + 5)
        print(f"{self.get_name()} enters a defensive stance, increasing armor class!")

    def regenerate_stamina(self):
        self.__current_stamina = min(self.__max_stamina, self.__current_stamina + self.__stamina_regeneration)

    def attack(self, target):
        self.basic_attack(target)

    def special_ability(self, target):
        self.defensive_stance()