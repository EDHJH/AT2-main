import pygame
import random

class Goblin:
    def __init__(self, position, window):
        """
        Initializes the Goblin object.

        Args:
            position (list): The initial position of the goblin [x, y].
            window (pygame.Surface): The game window surface.
        """
        self.__image = pygame.image.load("AT2/assets/mobs/goblinking.png").convert_alpha()  # Ensure the image path is correct
        self.__position = position  # Store the initial position of the goblin
        self.__window = window  # Store the game window object

    def move(self):
        """
        Moves the goblin randomly within a specified range and ensures it stays within the window bounds.
        """
        # Move the goblin randomly within a specified range
        self.__position[0] += random.randint(-10, 10)  # Randomly change the x-coordinate
        self.__position[1] += random.randint(-10, 10)  # Randomly change the y-coordinate

        # Ensure the goblin stays within the bounds of the window
        self.__position[0] = max(0, min(self.__window.get_width() - self.__image.get_width(), self.__position[0]))  # Clamp the x-coordinate
        self.__position[1] = max(0, min(self.__window.get_height() - self.__image.get_height(), self.__position[1]))  # Clamp the y-coordinate

    def draw(self):
        """
        Draws the goblin on the game window at its current position.
        """
        self.__window.blit(self.__image, self.__position)

    # Getter methods
    def get_image(self):
        return self.__image

    def get_position(self):
        return self.__position

    def get_window(self):
        return self.__window

    # Setter methods
    def set_position(self, position):
        self.__position = position

    def set_window(self, window):
        self.__window = window

