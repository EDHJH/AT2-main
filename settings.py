import pygame

class Settings:
    def __init__(self, window):
        """
        Initializes the Settings object.

        Args:
            window (pygame.Surface): The game window surface.
        """
        self.__window = window
        self.__font = pygame.font.Font(None, 36)
        self.__options = ["Volume", "Graphics", "Back"]
        self.__selected_option = 0

    def run(self):
        """
        Handles the display and interaction logic for the settings menu.
        """
        running = True
        while running:
            self.__window.fill((0, 0, 0))
            for index, option in enumerate(self.__options):
                color = (255, 0, 0) if index == self.__selected_option else (255, 255, 255)
                text = self.__font.render(option, 1, color)
                self.__window.blit(text, (50, 50 + index * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.__selected_option = (self.__selected_option + 1) % len(self.__options)
                    elif event.key == pygame.K_UP:
                        self.__selected_option = (self.__selected_option - 1) % len(self.__options)
                    elif event.key == pygame.K_RETURN:
                        if self.__options[self.__selected_option] == "Back":
                            return 'back'
                        else:
                            # Placeholder for setting adjustment functionality
                            print(f"Adjusting {self.__options[self.__selected_option]}")

        return None

    # Getter methods
    def get_window(self):
        return self.__window

    def get_font(self):
        return self.__font

    def get_options(self):
        return self.__options

    def get_selected_option(self):
        return self.__selected_option

    # Setter methods
    def set_window(self, window):
        self.__window = window

    def set_font(self, font):
        self.__font = font

    def set_options(self, options):
        self.__options = options

    def set_selected_option(self, selected_option):
        self.__selected_option = selected_option
