# ranger.py
from Characters.character import Character

class Ranger(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Ranger", armor=7, max_hp=max_hp)
        self.__max_stamina = 100
        self.__current_stamina = self.__max_stamina
        self.__stamina_regeneration = 10
        self.__strength = 10
        self.__attacks = {
            "Arrow Shot": {"method": self.arrow_shot, "stamina_cost": 10},
            "Charged Arrow": {"method": self.charged_arrow, "stamina_cost": 20},
            "Lightning Arrow": {"method": self.lightning_arrow, "stamina_cost": 25},
            "Rain of Arrows": {"method": self.rain_of_arrows, "stamina_cost": 50}
        }

    def arrow_shot(self, target):
        print(f"{self.get_name()} shoots an arrow at {target.get_name()}")
        target.take_damage(self.__strength)

    def charged_arrow(self, target):
        print(f"{self.get_name()} shoots a charged arrow at {target.get_name()}")
        target.take_damage(self.__strength * 1.5)

    def lightning_arrow(self, target):
        print(f"{self.get_name()} shoots a lightning arrow at {target.get_name()}")
        target.take_damage(self.__strength * 2)

    def rain_of_arrows(self, targets):
        for target in targets:
            print(f"{self.get_name()} rains arrows down on {target.get_name()}")
            target.take_damage(self.__strength * 0.5)

    def regenerate_stamina(self):
        self.__current_stamina = min(self.__max_stamina, self.__current_stamina + self.__stamina_regeneration)

    def attack(self, target):
        self.arrow_shot(target)

    def special_ability(self, target):
        self.rain_of_arrows([target])
