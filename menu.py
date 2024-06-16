import pygame
from assets import GAME_ASSETS

class MainMenu:
    def __init__(self, window):
        """
        Initializes the MainMenu object.

        Args:
            window (pygame.Surface): The game window surface.
        """
        self.__window = window
        self.__font = pygame.font.Font(None, 36)  # Specify the font size and style
        self.__menu_options = ['Start Game', 'Settings', 'Exit']
        self.__selected_option = 0  # The index of the currently selected menu option
        self.__background_image = pygame.image.load(GAME_ASSETS['kings_quest_titlescreen'])  # Load the background image
        # Scale the background image to match the window size
        self.__scaled_background = pygame.transform.scale(self.__background_image, (self.__window.get_width(), self.__window.get_height()))

    def run(self):
        """
        Handles the display and interaction logic for the main menu.
        """
        running = True
        while running:
            # Blit the scaled background image to fill the entire window
            self.__window.blit(self.__scaled_background, (0, 0))

            # Display each menu option on the screen
            for index, option in enumerate(self.__menu_options):
                # Highlight the selected option in red
                color = (255, 0, 0) if index == self.__selected_option else (255, 255, 255)
                text = self.__font.render(option, True, color)
                # Adjust the positioning of the text to be centered horizontally and slightly offset vertically
                text_rect = text.get_rect(center=(self.__window.get_width() / 2, 150 + 50 * index))
                self.__window.blit(text, text_rect)

            pygame.display.flip()  # Update the display with the new frame

            # Event handling in the menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'  # Return 'quit' if the window is closed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.__selected_option = (self.__selected_option + 1) % len(self.__menu_options)
                    elif event.key == pygame.K_UP:
                        self.__selected_option = (self.__selected_option - 1) % len(self.__menu_options)
                    elif event.key == pygame.K_RETURN:
                        # Return the current selected option when Enter is pressed
                        return self.__menu_options[self.__selected_option]

        return 'quit'  # Default return value if the loop ends

    # Getter methods
    def get_window(self):
        return self.__window

    def get_font(self):
        return self.__font

    def get_menu_options(self):
        return self.__menu_options

    def get_selected_option(self):
        return self.__selected_option

    def get_background_image(self):
        return self.__background_image

    def get_scaled_background(self):
        return self.__scaled_background

    # Setter methods
    def set_window(self, window):
        self.__window = window

    def set_font(self, font):
        self.__font = font

    def set_menu_options(self, menu_options):
        self.__menu_options = menu_options

    def set_selected_option(self, selected_option):
        self.__selected_option = selected_option

    def set_background_image(self, background_image):
        self.__background_image = background_image

    def set_scaled_background(self, scaled_background):
        self.__scaled_background = scaled_background

