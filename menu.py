import pygame
from assets import GAME_ASSETS

class MainMenu:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)  # Specify the font size and style
        self.menu_options = ['Start Game', 'Settings', 'Exit']
        self.selected_option = 0  # The index of the currently selected menu option
        self.background_image = pygame.image.load(GAME_ASSETS['kings_quest_titlescreen'])  # Load the background image
        # Scale the background image to match the window size
        self.scaled_background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
        self.button_rects = []  # List to store the Rects for the buttons

    def draw_buttons(self):
        self.button_rects = []
        for index, option in enumerate(self.menu_options):
            # Highlight the selected option in red
            color = (255, 0, 0) if index == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            # Adjust the positioning of the text to be centered horizontally and slightly offset vertically
            text_rect = text.get_rect(center=(self.window.get_width() / 2, 300 + 50 * index))
            self.window.blit(text, text_rect)
            # Store the Rect for each button
            self.button_rects.append(text_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    return self.menu_options[self.selected_option]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    mouse_pos = event.pos
                    for index, button_rect in enumerate(self.button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            return self.menu_options[index]
        return None

    def draw(self):
        """Handles the display logic for the main menu."""
        # Blit the scaled background image to fill the entire window
        self.window.blit(self.scaled_background, (0, 0))

        # Draw the buttons
        self.draw_buttons()

        pygame.display.flip()  # Update the display with the new frame