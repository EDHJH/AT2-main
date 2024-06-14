class Character:
    # Class constants
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level

    def __init__(self, name, character_class, armor):
        # Private attributes
        self.__name = name  
        self.__character_class = character_class  
        self.__armor = armor  
        self.__level = 1  
        self.__experience_points = 0 
        self.__hit_points = 10 
        self.__armor_class = 10 
        self.__skills = {} 
        self.__inventory = []  
        self.__gold = 0  
        self.__attribute_points = 0 

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

    # Setter Methods
    def set_name(self, name):
        self.__name = name

    def set_character_class(self, character_class):
        self.__character_class = character_class

    def set_armor(self, armor):
        self.__armor = armor

    def set_hit_points(self, hit_points):
        self.__hit_points = hit_points

    def set_armor_class(self, armor_class):
        self.__armor_class = armor_class

    def set_gold(self, gold):
        self.__gold = gold

    def assign_attribute_points(self, attribute, points):
        # Ensure the attribute exists before assigning points
        if attribute in self.__dict__:
            setattr(self, attribute, getattr(self, attribute) + points)  # Add points to the attribute
            self.__attribute_points -= points  # Decrease available attribute points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")

    def gain_experience(self, experience):
        self.__experience_points += experience  # Increase character's experience points
        # Calculate experience required for next level
        required_experience = self.calculate_required_experience(self.__level + 1)
        # Check if character has enough experience to level up and is below the level cap
        while self.__experience_points >= required_experience and self.__level < self.MAX_LEVEL:
            self.__level += 1  # Level up the character
            self.__experience_points -= required_experience  # Decrease character's experience points
            self.__hit_points += 10  # Example: Increase hit points by 10 each level up
            self.__attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.__name} is now level {self.__level}.")
            # Calculate experience required for next level
            required_experience = self.calculate_required_experience(self.__level + 1)

    def calculate_required_experience(self, level):
        # Example exponential scaling: Each level requires 100 more experience points than the previous level
        return int(100 * (1.5 ** (level - 1)))

    def is_alive(self):
        return self.__hit_points > 0

    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.__armor)
        self.__hit_points -= actual_damage
        if self.__hit_points <= 0:
            print(f"{self.__name} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.__name} takes {actual_damage} damage. Remaining hit points: {self.__hit_points}")
