import pygame
from main_menu import MainMenu
from character_select import CharacterSelect
from map import Map
from assets import load_assets, GAME_ASSETS

class Game:
    def __init__(self):
        pygame.init()
        load_assets()
        self.__window = pygame.display.set_mode((1366, 768))
        self.__menu = MainMenu(self.__window)
        self.__character_select = CharacterSelect(self.__window)
        self.__game_map = Map(self.__window)
        self.__state = 'menu'
        self.__current_character = None

    def run(self):
        while True:
            if self.__state == 'menu':
                result = self.__menu.run()
                if result == 'Start Game':
                    self.__state = 'character_select'
                elif result == 'Settings':
                    pass
                elif result == 'Exit':
                    pygame.quit()
                    return
            elif self.__state == 'character_select':
                selected_character = self.__character_select.run()
                if selected_character == 'back':
                    self.__state = 'menu'
                elif selected_character:
                    self.__current_character = selected_character
                    self.__game_map.load_player(selected_character)
                    self.__state = 'game_map'
            elif self.__state == 'game_map':
                result = self.__game_map.handle_events()
                if result == 'back':
                    self.__state = 'character_select'
                elif result == 'quit':
                    pygame.quit()
                    return
                else:
                    self.__game_map.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    # Getter and Setter methods
    def get_window(self):
        return self.__window

    def set_window(self, window):
        self.__window = window

    def get_menu(self):
        return self.__menu

    def set_menu(self, menu):
        self.__menu = menu

    def get_character_select(self):
        return self.__character_select

    def set_character_select(self, character_select):
        self.__character_select = character_select

    def get_game_map(self):
        return self.__game_map

    def set_game_map(self, game_map):
        self.__game_map = game_map

    def get_state(self):
        return self.__state

    def set_state(self, state):
        self.__state = state

    def get_current_character(self):
        return self.__current_character

    def set_current_character(self, current_character):
        self.__current_character = current_character

if __name__ == "__main__":
    game = Game()
    game.run()