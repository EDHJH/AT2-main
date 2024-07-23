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
    def choose_attack(self, target):
        print(f"Choose an attack (Current stamina: {self.get_current_stamina()}):")
        attack_list = list(self.get_attacks().items())
        for i, (attack, info) in enumerate(attack_list):
            print(f"{i + 1}. {attack} (Stamina cost: {info['stamina_cost']})")
        chosen_attack = int(input("Enter the number of the attack: "))
        if 1 <= chosen_attack <= len(attack_list):
            attack, attack_info = attack_list[chosen_attack - 1]
            if self.get_current_stamina() >= attack_info["stamina_cost"]:
                self.set_current_stamina(self.get_current_stamina() - attack_info["stamina_cost"])
                attack_method = attack_info["method"]
                attack_method(target)
            else:
                print("Not enough stamina for this attack.")
        else:
            print("Invalid attack.")

    def assign_attribute_points(self, attribute, points):
        if attribute in self.__dict__:
            setattr(self, attribute, getattr(self, attribute) + points)
            self.__attribute_points -= points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")

    def gain_experience(self, experience):
        self.__experience_points += experience
        required_experience = self.calculate_required_experience(self.__level + 1)
        while self.__experience_points >= required_experience and self.__level < self.MAX_LEVEL:
            self.__level += 1
            self.__experience_points -= required_experience
            self.__hit_points += 10
            self.__attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL
            print(f"Level up! {self.__name} is now level {self.__level}.")
            required_experience = self.calculate_required_experience(self.__level + 1)

    def calculate_required_experience(self, level):
        return int(100 * (1.5 ** (level - 1)))

    def is_alive(self):
        return self.__hit_points > 0

    def take_damage(self, amount):
        actual_damage = max(0, amount - self.get_armor())
        self.__hit_points -= actual_damage
        if self.__hit_points <= 0:
            print(f"{self.get_name()} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.get_name()} takes {actual_damage} damage. Remaining hit points: {self.__hit_points}")

    # Encapsulated attributes and methods for stamina
    def get_current_stamina(self):
        return self.__current_stamina

    def set_current_stamina(self, value):
        self.__current_stamina = value

    def get_attacks(self):
        return self.__attacks
