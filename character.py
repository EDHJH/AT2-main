import pygame
# character.py

class Character:
    MAX_LEVEL = 50
    ATTRIBUTE_POINTS_PER_LEVEL = 3

    def __init__(self, name, character_class, armor, max_hp):
        self.__name = name
        self.__character_class = character_class
        self.__armor = armor
        self.__level = 1
        self.__experience_points = 0
        self.__hit_points = max_hp
        self.__armor_class = armor
        self.__skills = {}
        self.__inventory = []
        self.__gold = 0
        self.__attribute_points = 0

    # Getter and Setter methods
    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_character_class(self):
        return self.__character_class

    def set_character_class(self, character_class):
        self.__character_class = character_class

    def get_armor(self):
        return self.__armor

    def set_armor(self, armor):
        self.__armor = armor

    def get_hit_points(self):
        return self.__hit_points

    def set_hit_points(self, hit_points):
        self.__hit_points = hit_points

    def get_armor_class(self):
        return self.__armor_class

    def set_armor_class(self, armor_class):
        self.__armor_class = armor_class

    def get_experience_points(self):
        return self.__experience_points

    def set_experience_points(self, experience_points):
        self.__experience_points = experience_points

    def get_level(self):
        return self.__level

    def get_skills(self):
        return self.__skills

    def get_inventory(self):
        return self.__inventory

    def get_gold(self):
        return self.__gold

    def set_gold(self, gold):
        self.__gold = gold

    def get_attribute_points(self):
        return self.__attribute_points

    def assign_attribute_points(self, attribute, points):
        if hasattr(self, f"_{self.__class__.__name__}__{attribute}") and points > 0 and self.__attribute_points >= points:
            setattr(self, f"_{self.__class__.__name__}__{attribute}", getattr(self, f"_{self.__class__.__name__}__{attribute}") + points)
            self.__attribute_points -= points
        else:
            print(f"Error: Cannot assign {points} points to attribute '{attribute}'.")

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
        actual_damage = max(0, amount - self.__armor)
        self.__hit_points -= actual_damage
        if self.__hit_points <= 0:
            print(f"{self.__name} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.__name} takes {actual_damage} damage. Remaining hit points: {self.__hit_points}")

    def draw_health_bar(self, window, x, y):
        bar_width = 100
        bar_height = 10
        fill = (self.__hit_points / 10) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(window, (255, 0, 0), fill_rect)
        pygame.draw.rect(window, (255, 255, 255), outline_rect, 2)

    def attack(self, target):
        raise NotImplementedError("Subclasses should implement this method")

    def special_ability(self, target):
        raise NotImplementedError("Subclasses should implement this method")
