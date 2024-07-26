class Character:
    MAX_LEVEL = 10  # Maximum level a character can reach

    def __init__(self, name, character_class, armor):
        self.__name = name  # Character's name
        self.__character_class = character_class  # Character's class
        self.__armor = armor  # Character's armor value
        self.__level = 1  # Character's current level
        self.__experience_points = 0  # Character's current experience points
        self.__hit_points = 10 
        self.__armor_class = 10  
        self.__current_hp = self.__hit_points  # Example starting current HP
        self.__current_stamina = 100  # Example starting current stamina
        self.__max_stamina = 100  # Example maximum stamina
        self.__strength = 1  
        self.__attacks = {}  # Example attacks

    # Getter methods
    def get_name(self):
        return self.__name

    def get_character_class(self):
        return self.__character_class

    def get_armor(self):
        return self.__armor

    def get_level(self):
        return self.__level

    def get_experience_points(self):
        return self.__experience_points

    def get_hit_points(self):
        return self.__hit_points

    def get_armor_class(self):
        return self.__armor_class

    def get_skills(self):
        return self.__skills

    def get_inventory(self):
        return self.__inventory

    def get_gold(self):
        return self.__gold

    def get_current_hp(self):
        return self.__current_hp

    def get_current_stamina(self):
        return self.__current_stamina

    def get_max_hp(self):
        return self.__hit_points

    def get_max_stamina(self):
        return self.__max_stamina

    def get_strength(self):
        return self.__strength

    def get_attacks(self):
        return self.__attacks

    # Setter methods
    def set_armor(self, value):
        if value >= 0:
            self.__armor = value
        else:
            raise ValueError("Armor value must be non-negative")

    def set_armor_class(self, value):
        if value >= 0:
            self.__armor_class = value
        else:
            raise ValueError("Armor class value must be non-negative")

    def set_gold(self, value):
        if value >= 0:
            self.__gold = value
        else:
            raise ValueError("Gold value must be non-negative")

    # Functions
    def choose_attack(self, target, attack_name=None):
        if attack_name is None:  # Basic attack
            attack_method = self.basic_attack
            stamina_cost = 0
        else:  # Special attack
            attack_method = self.__attacks[attack_name]["method"]
            stamina_cost = self.__attacks[attack_name]["stamina_cost"]

        if self.get_current_stamina() >= stamina_cost:
            self._current_stamina -= stamina_cost
            return attack_method(target)
        else:
            print("Not enough stamina for this attack.")
            return 0

    def increase_max_hp(self, amount):
        self.__hit_points += amount
        self.__current_hp += amount  # Optionally heal the player

    def increase_max_stamina(self, amount):
        self.__max_stamina += amount

    def increase_strength(self, amount):
        self.__strength += amount

    def level_up(self):
        self.__level += 1
        self.__hit_points += 10  # Increase max health by 10
        self.__max_stamina += 20  # Increase max stamina by 20
        self.__strength += 1  # Increase strength by 1
        self.__current_hp = self.__hit_points  # Optionally heal the player to full health
        print(f"Level up! {self.get_name()} is now level {self.__level}.")

    def calculate_required_experience(self, level):
        return int(100 * (1.5 ** (level - 1)))

    def is_alive(self):
        return self.__current_hp > 0

    def take_damage(self, amount):
        actual_damage = max(0, amount - self.__armor)
        self.__current_hp -= actual_damage
        if self.__current_hp <= 0:
            print(f"{self.__name} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.__name} takes {actual_damage} damage. Remaining hit points: {self.__current_hp}")
