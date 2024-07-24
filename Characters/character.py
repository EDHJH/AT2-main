class Character:
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level

    def __init__(self, name, character_class, armor):
        self.__name = name  # Character's name
        self.__character_class = character_class  # Character's class
        self.__armor = armor  # Character's armor value
        self.__level = 1  # Character's current level
        self.__experience_points = 0  # Character's current experience points
        self.__hit_points = 10  # Example starting value for character's hit points
        self.__armor_class = 10  # Example starting value for character's armor class
        self.__skills = {}  # Example empty dictionary for character's skills
        self.__inventory = []  # Example empty list for character's inventory
        self.__gold = 0  # Example starting value for character's gold
        self.__attribute_points = 0  # Attribute points available to allocate
        self.__current_hp = self.__hit_points  # Example starting current HP
        self.__current_stamina = 100  # Example starting current stamina
        self.__max_stamina = 100  # Example maximum stamina
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

    def get_attribute_points(self):
        return self.__attribute_points

    def get_current_hp(self):
        return self.__current_hp

    def get_current_stamina(self):
        return self.__current_stamina

    def get_max_hp(self):
        return self.__hit_points

    def get_max_stamina(self):
        return self.__max_stamina

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


    def assign_attribute_points(self, attribute, points):
        if attribute in self.__dict__:
            setattr(self, attribute, getattr(self, attribute) + points)  # Add points to the attribute
            self.__attribute_points -= points  # Decrease available attribute points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")

    def gain_experience(self, experience):
        self.__experience_points += experience  # Increase character's experience points
        required_experience = self.calculate_required_experience(self.__level + 1)
        while self.__experience_points >= required_experience and self.__level < self.MAX_LEVEL:
            self.__level += 1  # Level up the character
            self.__experience_points -= required_experience  # Decrease character's experience points
            self.__hit_points += 10  # Example: Increase hit points by 10 each level up
            self.__attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.__name} is now level {self.__level}.")
            required_experience = self.calculate_required_experience(self.__level + 1)

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
