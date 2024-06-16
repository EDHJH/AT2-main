import pygame
import random

class Enemy:
    # Class-level private attributes
    __image = None
    __position = None
    __window = None
    __health = None

    def __init__(self, image_path, position, window):
        # Load the enemy image from the specified image path
        self.__image = pygame.image.load(image_path).convert_alpha()
        
        # Scale the enemy image to 0.75 times the original size
        self.__image = pygame.transform.scale(self.__image, (int(self.__image.get_width() * 0.75), int(self.__image.get_height() * 0.75)))
        
        # Set the initial position of the enemy
        self.__position = position
        
        # Set the window where the enemy will be drawn
        self.__window = window
        
        # Set the initial health of the enemy to 100
        self.__health = 100

    def take_damage(self, damage):
        """
        Reduces the enemy's health by the specified damage amount.

        Args:
            damage (int): The amount of damage to inflict.

        Returns:
            bool: True if the enemy's health is less than or equal to 0, indicating that it is defeated.
        """
        self.__health -= damage
        return self.__health <= 0

    def draw(self):
        """
        Draws the enemy on the window at its current position.
        Adjusts the position to ensure the image does not overflow the window boundaries.
        """
        adjusted_position = [
            max(0, min(self.__window.get_width() - self.__image.get_width(), self.__position[0])),
            max(0, min(self.__window.get_height() - self.__image.get_height(), self.__position[1]))
        ]
        
        self.__window.blit(self.__image, adjusted_position)

    # Getter methods
    def get_image(self):
        return self.__image

    def get_position(self):
        return self.__position

    def get_window(self):
        return self.__window

    def get_health(self):
        return self.__health

    # Setter methods
    def set_position(self, position):
        self.__position = position

    def set_health(self, health):
        self.__health = health
