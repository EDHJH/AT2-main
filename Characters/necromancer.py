from Characters.character import Character

class Necromancer(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Necromancer", armor=7)
        self.__max_stamina = 100
        self.__current_stamina = self.__max_stamina
        self.__stamina_regeneration = 10
        self.__strength = 10
        self.__max_hp = max_hp
        self.__current_hp = max_hp
        self.__attacks = {
            "Reap": {"method": self.reap, "stamina_cost": 10},
            "Dark Blast": {"method": self.dark_blast, "stamina_cost": 20},
            "Soul Drain": {"method": self.soul_drain, "stamina_cost": 25},
            "Plague": {"method": self.plague, "stamina_cost": 50}
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

    def reap(self, target):
        print(f"{self.get_name()} reaps the soul of {target.get_name()}!")
        damage = self.__strength
        target.take_damage(damage)
        self.__current_hp = min(self.__max_hp, self.__current_hp + damage * 0.3)  # Heal 30% of the damage dealt

    def dark_blast(self, target):
        print(f"{self.get_name()} unleashes a dark blast at {target.get_name()}!")
        damage = self.__strength * 1.5
        target.take_damage(damage)

    def soul_drain(self, target):
        print(f"{self.get_name()} drains the soul of {target.get_name()}!")
        damage = self.__strength * 2
        self.__current_hp = min(self.__max_hp, self.__current_hp + damage * 0.5)  # Heal half of the damage dealt
        target.take_damage(damage)

    def plague(self, targets):
        total_damage = 0
        for target in targets:
            damage = self.__strength * 0.75
            total_damage += damage
            print(f"{self.get_name()} spreads a plague to {target.get_name()}!")
            target.take_damage(damage)
        print(f"{self.get_name()} dealt a total of {total_damage} damage with plague!")
