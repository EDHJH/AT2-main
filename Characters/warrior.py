from Characters.character import Character

class Warrior(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Warrior", armor=6)
        self.__max_stamina = 100
        self.__current_stamina = self.__max_stamina
        self.__stamina_regeneration = 5
        self.__strength = 100
        self.__max_hp = max_hp
        self.__current_hp = max_hp
        self.__attacks = {
            "Charge": {"method": self.charge, "stamina_cost": 20},
            "Cleave Attack": {"method": self.cleave_attack, "stamina_cost": 30},
            "Shield Bash": {"method": self.shield_bash, "stamina_cost": 15},
            "Execute": {"method": self.Execute, "stamina_cost": 40}
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
    
    def charge(self, target):
        print(f"\n{self.get_name()} charges towards {target.get_name()}!")
        damage = self.__strength
        target.take_damage(damage)
        return damage

    def cleave_attack(self, target):
        print(f"\n{self.get_name()} cleaves {target.get_name()}!")
        damage = self.__strength * 2
        target.take_damage(damage)
        return damage

    def shield_bash(self, target):
        print(f"\n{self.get_name()} performs a shield bash on {target.get_name()}!")
        damage = self.__strength + 5
        target.take_damage(damage)
        return damage

    def Execute(self, target):
        print(f"\n{self.get_name()} performs a shield bash on {target.get_name()}!")
        damage = self.__strength *3
        target.take_damage(damage)
        return damage

    def consume_stamina(self, amount):
        self.__current_stamina = max(0, self.__current_stamina - amount)

    def heal(self, amount):
        self.__current_hp = min(self.__max_hp, self.__current_hp + amount)

    def regenerate_stamina(self, full=False):
        if full:
            self.__current_stamina = self.__max_stamina  # Fully regenerate stamina
        else:
            self.__current_stamina = min(self.__max_stamina, self.__current_stamina + self.__stamina_regeneration)
