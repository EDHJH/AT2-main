from Characters.character import Character

class Ranger(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Ranger", armor=7)
        self.__max_stamina = 100
        self.__current_stamina = self.__max_stamina
        self.__stamina_regeneration = 10
        self.__strength = 10
        self.__max_hp = max_hp
        self.__current_hp = max_hp
        self.__attacks = {
            "Basic Attack": {"method": self.basic_attack, "stamina_cost": 0},
            "Arrow Shot": {"method": self.arrow_shot, "stamina_cost": 10},
            "Charged Arrow": {"method": self.charged_arrow, "stamina_cost": 20},
            "Lightning Arrow": {"method": self.lightning_arrow, "stamina_cost": 25},
            "Rain of Arrows": {"method": self.rain_of_arrows, "stamina_cost": 50}
        }

    # Getter Methods
    def get_max_stamina(self):
        return self.__max_stamina

    def get_current_stamina(self):
        return self.__current_stamina

    def get_stamina_regeneration(self):
        return self.__stamina_regeneration

    def get_strength(self):
        return self.__strength

    def get_attacks(self):
        return self.__attacks

    def get_max_hp(self):
        return self.__max_hp

    def get_current_hp(self):
        return self.__current_hp

    def take_damage(self, amount):
        actual_damage = max(0, amount - self.get_armor())
        self.__current_hp -= actual_damage
        if self.__current_hp <= 0:
            print(f"{self.get_name()} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.get_name()} takes {actual_damage} damage. Remaining hit points: {self.__current_hp}")

    # Functions
    def regenerate_stamina(self):
        self.__current_stamina = min(self.__max_stamina, self.__current_stamina + self.__stamina_regeneration)

    def basic_attack(self, target):
        print(f"{self.get_name()} attacks {target.get_name()} with a basic attack!")
        damage = self.__strength
        target.take_damage(damage)
        return damage

    def arrow_shot(self, target):
        print(f"\n{self.get_name()} shoots an arrow at {target.get_name()}!")
        damage = self.__strength
        target.take_damage(damage)
        return damage

    def charged_arrow(self, target):
        print(f"\n{self.get_name()} shoots a charged arrow at {target.get_name()}!")
        damage = self.__strength * 1.5
        target.take_damage(damage)
        return damage

    def lightning_arrow(self, target):
        print(f"\n{self.get_name()} shoots a lightning arrow at {target.get_name()}!")
        damage = self.__strength * 2
        target.take_damage(damage)
        return damage

    def rain_of_arrows(self, target):
        print(f"\n{self.get_name()} rains arrows down on {target.get_name()}!")
        damage = self.__strength * 0.5
        target.take_damage(damage)
        return damage
