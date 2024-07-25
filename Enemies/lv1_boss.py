import pygame, random
from Enemies.enemy import Enemy  # Import the base Enemy class

class lv1_Boss:
    def __init__(self, image_path, position, window):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.position = position
        self.window = window
        self.health = 500  # Boss health, adjust as needed

    def draw(self, window):
        window.blit(self.image, self.position)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def is_defeated(self):
        return self.health <= 0

    def attack(self, target):
        damage = random.randint(10, 20)  # Boss damage range
        target.take_damage(damage)
        return damage
