import pygame
from Enemies.enemy import Enemy

class Orc(Enemy):
    def __init__(self, position, window):
        super().__init__('AT2/assets/orc.png', position, window, name="Orc")