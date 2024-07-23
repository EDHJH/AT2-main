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
    def getName(self):
        return self.__name

    def getCharacter_class(self):
        return self.__character_class

    def getArmor(self):
        return self.__armor

    def getLevel(self):
        return self.__level

    def getExperience_points(self):
        return self.__experience_points

    def getHit_points(self):
        return self.__hit_points

    def getArmor_class(self):
        return self.__armor_class

    def getSkills(self):
        return self.__skills

    def getInventory(self):
        return self.__inventory

    def getGold(self):
        return self.__gold

    def getAttribute_points(self):
        return self.__attribute_points

    # Setter methods
    def setArmor(self, value):
        if value >= 0:
            self.__armor = value
        else:
            raise ValueError("Armor value must be non-negative")

    def setArmor_class(self, value):
        if value >= 0:
            self.__armor_class = value
        else:
            raise ValueError("Armor class value must be non-negative")

    def setGold(self, value):
        if value >= 0:
            self.__gold = value
        else:
            raise ValueError("Gold value must be non-negative")
    
    # Functions
    def choose_attack(self, target):
        print(f"Choose an attack (Current stamina: {self.current_stamina}):")
        attack_list = list(self.attacks.items())
        for i, (attack, info) in enumerate(attack_list):
            print(f"{i + 1}. {attack} (Stamina cost: {info['stamina_cost']})")
        chosen_attack = int(input("Enter the number of the attack: "))
        if 1 <= chosen_attack <= len(attack_list):
            attack, attack_info = attack_list[chosen_attack - 1]
            if self.current_stamina >= attack_info["stamina_cost"]:
                self.current_stamina -= attack_info["stamina_cost"]
                attack_method = attack_info["method"]
                attack_method(target)
            else:
                print("Not enough stamina for this attack.")
        else:
            print("Invalid attack.")
    
    def assign_attribute_points(self, attribute, points):
        # Ensure the attribute exists before assigning points
        if attribute in self.__dict__:
            setattr(self, attribute, getattr(self, attribute) + points)  # Add points to the attribute
            self.getAttribute_points -= points  # Decrease available attribute points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")

    def gain_experience(self, experience):
        self.getExperience_points += experience  # Increase character's experience points
        # Calculate experience required for next level
        required_experience = self.calculate_required_experience(self.getLevel + 1)
        # Check if character has enough experience to level up and is below the level cap
        while self.getExperience_points >= required_experience and self.getLevel < self.MAX_LEVEL:
            self.getLevel += 1  # Level up the character
            self.getExperience_points -= required_experience  # Decrease character's experience points
            self.getHit_points += 10  # Example: Increase hit points by 10 each level up
            self.getAttribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.getName} is now level {self.getLevel}.")
            # Calculate experience required for next level
            required_experience = self.calculate_required_experience(self.level + 1)

    def calculate_required_experience(self, level):
        # Example exponential scaling: Each level requires 100 more experience points than the previous level
        return int(100 * (1.5 ** (level - 1)))

    def is_alive(self):
        return self.getHit_points > 0

    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.getArmor)
        self.getHit_points -= actual_damage
        if self.getHit_points <= 0:
            print(f"{self.getName} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.getName} takes {actual_damage} damage. Remaining hit points: {self.getHit_points}")
