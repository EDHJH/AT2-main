# main_menu.py
import pygame
from assets import GAME_ASSETS

class MainMenu:
    def __init__(self, window):
        self.__window = window
        self.__font = pygame.font.Font(None, 36)
        self.__menu_options = ['Start Game', 'Settings', 'Exit']
        self.__selected_option = 0
        self.__background_image = pygame.image.load(GAME_ASSETS['kings_quest_titlescreen'])
        self.__scaled_background = pygame.transform.scale(self.__background_image, (self.__window.get_width(), self.__window.get_height()))

    def run(self):
        running = True
        while running:
            self.__window.blit(self.__scaled_background, (0, 0))
            for index, option in enumerate(self.__menu_options):
                color = (255, 0, 0) if index == self.__selected_option else (255, 255, 255)
                text = self.__font.render(option, True, color)
                text_rect = text.get_rect(center=(self.__window.get_width() / 2, 150 + 50 * index))
                self.__window.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.__selected_option = (self.__selected_option + 1) % len(self.__menu_options)
                    elif event.key == pygame.K_UP:
                        self.__selected_option = (self.__selected_option - 1) % len(self.__menu_options)
                    elif event.key == pygame.K_RETURN:
                        return self.__menu_options[self.__selected_option]
        return 'quit'

    # Getter and Setter methods
    def get_window(self):
        return self.__window

    def set_window(self, window):
        self.__window = window

    def get_font(self):
        return self.__font

    def set_font(self, font):
        self.__font = font

    def get_menu_options(self):
        return self.__menu_options

    def set_menu_options(self, menu_options):
        self.__menu_options = menu_options

    def get_selected_option(self):
        return self.__selected_option

    def set_selected_option(self, selected_option):
        self.__selected_option = selected_option

    def get_background_image(self):
        return self.__background_image

    def set_background_image(self, background_image):
        self.__background_image = background_image

    def get_scaled_background(self):
        return self.__scaled_background

    def set_scaled_background(self, scaled_background):
        self.__scaled_background = scaled_background