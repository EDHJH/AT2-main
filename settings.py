import pygame

class Settings:
    def __init__(self, window):
        self.__window = window
        self.__font = pygame.font.Font(None, 36)
        self.__options = ["Volume", "Graphics", "Back"]
        self.__selected_option = 0

    def run(self):
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
                            print(f"Adjusting {self.__options[self.__selected_option]}")
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

    def get_options(self):
        return self.__options

    def set_options(self, options):
        self.__options = options

    def get_selected_option(self):
        return self.__selected_option

    def set_selected_option(self, selected_option):
        self.__selected_option = selected_option
