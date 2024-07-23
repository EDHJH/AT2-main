import pygame
from Enemies.enemy import Enemy

class Goblin(Enemy):
    def __init__(self, position, window):
        super().__init__('AT2/assets/goblin.png', position, window, name="Goblin")
