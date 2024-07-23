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
            "Summon Skeleton": {"method": self.summon_skeleton, "stamina_cost": 10},
            "Dark Blast": {"method": self.dark_blast, "stamina_cost": 20},
            "Soul Drain": {"method": self.soul_drain, "stamina_cost": 25},
            "Plague": {"method": self.plague, "stamina_cost": 50}
        }

    # Getter Methods
    def getMax_stamina(self):
        return self.__max_stamina

    def getCurrent_stamina(self):
        return self.__current_stamina

    def getStamina_regeneration(self):
        return self.__stamina_regeneration

    def getStrength(self):
        return self.__strength

    def getAttacks(self):
        return self.__attacks

    def getMax_hp(self):
        return self.__max_hp

    def getCurrent_hp(self):
        return self.__current_hp

    # Functions
    def regenerate_stamina(self):
        self.__current_stamina = min(self.__max_stamina, self.__current_stamina + self.__stamina_regeneration)

    def attack(self, target):
        damage = self.__strength * self.getLevel()
        target.take_damage(damage)
        return damage

    def summon_skeleton(self, target):
        print(f"{self.getName()} summons a skeleton to attack {target.getName()}!")
        damage = self.__strength
        target.take_damage(damage)

    def dark_blast(self, target):
        print(f"{self.getName()} unleashes a dark blast at {target.getName()}!")
        damage = self.__strength * 1.5
        target.take_damage(damage)

    def soul_drain(self, target):
        print(f"{self.getName()} drains the soul of {target.getName()}!")
        damage = self.__strength * 2
        self.__current_hp = min(self.__max_hp, self.__current_hp + damage * 0.5)  # Heal half of the damage dealt
        target.take_damage(damage)

    def plague(self, targets):
        total_damage = 0
        for target in targets:
            damage = self.__strength * 0.75
            total_damage += damage
            print(f"{self.getName()} spreads a plague to {target.getName()}!")
            target.take_damage(damage)
        print(f"{self.getName()} dealt a total of {total_damage} damage with plague!")
