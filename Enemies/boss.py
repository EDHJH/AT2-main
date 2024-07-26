import pygame
import random
from Enemies.enemy import Enemy  # Import the base Enemy class

class Boss(Enemy):
    def __init__(self, image_path, position, window):
        super().__init__(image_path, position, window, hp=500, damage=20, armor=10, name='Boss')

    def draw(self):
        self.window.blit(self.image, self.position)
