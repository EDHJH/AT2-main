# character_select.py
import pygame
from assets import GAME_ASSETS

class CharacterSelect:
    """
    A class representing the character selection screen.
    """

    def __init__(self, window):
        """
        Initializes the CharacterSelect object.

        Args:
            window (pygame.Surface): The game window surface.
        """
        self.__window = window
        self.__font = pygame.font.Font(None, 36)  # Use a default font
        self.__background_image = pygame.image.load(GAME_ASSETS['main_menu_background']).convert()
        self.__background_image = pygame.transform.scale(self.__background_image, (self.__window.get_width(), self.__window.get_height()))
        self.__characters = {
            "Warrior": pygame.image.load(GAME_ASSETS['warrior_button']).convert_alpha(),
            "Mage": pygame.image.load(GAME_ASSETS['mage_button']).convert_alpha(),
            "Rogue": pygame.image.load(GAME_ASSETS['rogue_button']).convert_alpha()
        }
        self.__character_buttons = self.__setup_character_buttons()
        self.__back_button = pygame.Rect(50, self.__window.get_height() - 50 - 30, 100, 30)  # Positioned at bottom left

    def __setup_character_buttons(self):
        """
        Sets up the character buttons.

        Returns:
            dict: A dictionary mapping character names to their button rectangles.
        """
        buttons = {}
        total_spacing = 40  # spacing between buttons and edges
        num_buttons = len(self.__characters)
        available_width = self.__window.get_width() - total_spacing * (num_buttons + 1)
        button_width = available_width // num_buttons
        max_height = self.__window.get_height() // 4  # maximum button height

        x = total_spacing
        y = self.__window.get_height() // 3 - max_height // 2  # position them a bit higher to make space for back button

        for character, image in self.__characters.items():
            aspect_ratio = image.get_height() / image.get_width()
            button_height = int(button_width * aspect_ratio)
            button_height = min(button_height, max_height)  # Ensure button isn't too tall
            scaled_image = pygame.transform.scale(image, (button_width, button_height))
            buttons[character] = (scaled_image, pygame.Rect(x, y, button_width, button_height))
            x += button_width + total_spacing

        return buttons

    def run(self):
        running = True
        while running:
            self.__window.blit(self.__background_image, (0, 0))
            for character, (image, rect) in self.__character_buttons.items():
                self.__window.blit(image, rect)

            # Draw back button
            pygame.draw.rect(self.__window, (200, 200, 200), self.__back_button)  # Draw a grey button
            back_text = self.__font.render('Back', True, (0, 0, 0))
            text_rect = back_text.get_rect(center=self.__back_button.center)
            self.__window.blit(back_text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__back_button.collidepoint(event.pos):
                        return 'back'
                    for character, (image, rect) in self.__character_buttons.items():
                        if rect.collidepoint(event.pos):
                            return character

        return None

    # Getter and Setter methods
    def get_window(self):
        return self.__window

    def set_window(self, window):
        self.__window = window

    def get_font(self):
        return self.__font

    def set_font(self, font):
        self.__font = font

    def get_background_image(self):
        return self.__background_image

    def set_background_image(self, background_image):
        self.__background_image = background_image

    def get_characters(self):
        return self.__characters

    def set_characters(self, characters):
        self.__characters = characters

    def get_character_buttons(self):
        return self.__character_buttons

    def set_character_buttons(self, character_buttons):
        self.__character_buttons = character_buttons

    def get_back_button(self):
        return self.__back_button

    def set_back_button(self, back_button):
        self.__back_button = back_button
