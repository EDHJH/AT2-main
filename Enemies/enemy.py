import pygame
import random

class Enemy:
    def __init__(self, image_path, position, window, name="Enemy"):
        self.image_path = image_path  # Save the image path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.75), int(self.image.get_height() * 0.75)))
        self.position = position
        self.window = window
        self.health = 100
        self.max_health = 100  # Add max_health attribute
        self.name = name

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

    def draw(self):
        adjusted_position = [
            max(0, min(self.window.get_width() - self.image.get_width(), self.position[0])),
            max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))
        ]
        self.window.blit(self.image, adjusted_position)

    def get_name(self):
        return self.name

    def get_hit_points(self):
        return self.health

    def get_max_hp(self):  # Add get_max_hp method
        return self.max_health

    def get_current_hp(self):  # Add get_current_hp method
        return self.health

    def get_image_path(self):  # Add get_image_path method
        return self.image_path

    def attack(self, target):
        damage = random.randint(5, 15)  # Random damage between 5 and 15
        print(f"\n{self.get_name()} attacks {target.get_name()} and deals {damage} damage!")
        target.take_damage(damage)
        return damage
