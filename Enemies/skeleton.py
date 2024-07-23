import pygame
from Enemies.enemy import Enemy

class Skeleton(Enemy):
    def __init__(self, position, window):
        super().__init__('AT2/assets/skeleton.png', position, window, name="Skeleton")
