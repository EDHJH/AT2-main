# enemy.py
import pygame

class Enemy:
    def __init__(self, image_path, position, window):
        self.__image = pygame.image.load(image_path).convert_alpha()
        self.__image = pygame.transform.scale(self.__image, (int(self.__image.get_width() * 0.75), int(self.__image.get_height() * 0.75)))
        self.__position = position
        self.__window = window
        self.__health = 100

    def take_damage(self, damage):
        self.__health -= damage
        return self.__health <= 0

    def draw(self):
        adjusted_position = [
            max(0, min(self.__window.get_width() - self.__image.get_width(), self.__position[0])),
            max(0, min(self.__window.get_height() - self.__image.get_height(), self.__position[1]))
        ]
        self.__window.blit(self.__image, adjusted_position)
        self.draw_health_bar(self.__window, adjusted_position[0], adjusted_position[1] - 10)

    def draw_health_bar(self, window, x, y):
        bar_width = 50
        bar_height = 5
        fill = (self.__health / 100) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(window, (255, 0, 0), fill_rect)
        pygame.draw.rect(window, (255, 255, 255), outline_rect, 1)

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

    def set_window(self, window):
        self.__window = window

    def set_health(self, health):
        self.__health = health