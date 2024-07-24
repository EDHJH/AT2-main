import pygame
from assets import GAME_ASSETS

class Turnbased:
    def __init__(self, player, enemy, window):
        self.player = player
        self.enemy = enemy
        self.window = window
        self.player_turn = True
        self.turn_background_image = pygame.image.load(GAME_ASSETS["lv1_turn_background"]).convert()
        self.turn_background_image = pygame.transform.scale(self.turn_background_image, (self.window.get_width(), self.window.get_height()))
        self.panel_image = pygame.image.load(GAME_ASSETS["panel"]).convert_alpha()
        self.panel_image = pygame.transform.scale(self.panel_image, (self.window.get_width(), 150))  # Adjust the height as needed
        self.ground_image = pygame.image.load(GAME_ASSETS["ground"]).convert()
        self.ground_image_width, self.ground_image_height = self.ground_image.get_size()

        # Load the custom font
        self.font_path = "assets/slkscre.ttf"  # Path to the TTF file
        self.font_stats = pygame.font.Font(self.font_path, 36)  # Default font for player stats

        self.selected_attack = 0
        self.showing_special_attacks = False

        # Load player image
        self.player_image = pygame.image.load(GAME_ASSETS[f"{self.player.get_character_class().lower()}"]).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.75), int(self.player_image.get_height() * 0.75)))

        # Load enemy image
        enemy_image_path = self.enemy.get_image_path()
        self.enemy_image = pygame.image.load(enemy_image_path).convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (int(self.enemy_image.get_width() * 0.75), int(self.enemy_image.get_height() * 0.75)))

    def draw_health_bar(self, entity, x, y, width, height):
        # Calculate health percentage
        health_percentage = entity.get_current_hp() / entity.get_max_hp()

        # Calculate the width of the health bar
        health_bar_width = int(width * health_percentage)

        # Draw the health bar background
        pygame.draw.rect(self.window, (255, 0, 0), (x, y, width, height))  # Red background

        # Draw the current health
        pygame.draw.rect(self.window, (0, 255, 0), (x, y, health_bar_width, height))  # Green health

    def draw_combat_ui(self):
        self.window.blit(self.turn_background_image, (0, 0))

        # Draw ground image just above the panel, repeating it to fill the width
        ground_y_position = self.window.get_height() - 200
        for x in range(0, self.window.get_width(), self.ground_image_width):
            self.window.blit(self.ground_image, (x, ground_y_position))

        self.window.blit(self.panel_image, (0, self.window.get_height() - 150))  # Position the panel at the bottom

        # Draw player and enemy just above the ground
        player_pos = (self.window.get_width() * 0.25 - self.player_image.get_width() // 2, ground_y_position - self.player_image.get_height())
        enemy_pos = (self.window.get_width() * 0.75 - self.enemy_image.get_width() // 2, ground_y_position - self.enemy_image.get_height())
        self.window.blit(self.player_image, player_pos)
        self.window.blit(self.enemy_image, enemy_pos)

        # Draw player health bar above the player image
        self.draw_health_bar(self.player, player_pos[0], player_pos[1] - 20, self.player_image.get_width(), 10)

        # Draw enemy health bar above the enemy image
        self.draw_health_bar(self.enemy, enemy_pos[0], enemy_pos[1] - 20, self.enemy_image.get_width(), 10)

        # Draw player stats on the left half of the panel
        self.draw_player_stats()

        # Draw attack options on the right half of the panel
        self.draw_attack_options()

        pygame.display.flip()

    def draw_player_stats(self):
        panel_top = self.window.get_height() - 150
        # Draw player stats on top of the panel
        stats_text = [
            f"Name: {self.player.get_name()}",
            f"Class: {self.player.get_character_class()}",
            f"HP: {self.player.get_current_hp()}/{self.player.get_max_hp()}",
            f"Stamina: {self.player.get_current_stamina()}/{self.player.get_max_stamina()}"
        ]

        for i, text in enumerate(stats_text):
            rendered_text = self.font_stats.render(text, True, (255, 255, 255))
            self.window.blit(rendered_text, (20, panel_top + 20 + i * 30))

    def draw_attack_options(self):
        panel_top = self.window.get_height() - 150

        if not self.showing_special_attacks:
            # Draw main attack options
            options = ["Attack", "Special Attacks", "Use Items", "Run"]
        else:
            # Draw special attack options
            attacks = self.player.get_attacks()
            attack_list = list(attacks.items())
            options = [attack for attack, info in attack_list]

        self.button_rects = []
        button_width = 200
        button_height = 50
        padding_x = 40  # Increased horizontal padding
        padding_y = 20
        start_x = self.window.get_width() // 2 + 60  # Moved more to the right
        start_y = panel_top + 20

        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position

        for i, option in enumerate(options):
            rect_x = start_x + (i % 2) * (button_width + padding_x + (50 if i in [1, 3] else 0))  # Adjust x position for Special Attacks and Run buttons
            rect_y = start_y + (i // 2) * (button_height + padding_y)
            rect = pygame.Rect(rect_x, rect_y, button_width, button_height)
            
            if rect.collidepoint(mouse_pos):
                color = (0, 0, 255)  # Blue color when hovered
            else:
                color = (255, 255, 255)  # White color

            pygame.draw.rect(self.window, color, rect, 2)  # Draw button rectangle
            font = self.find_font_size(option, button_width - 10, button_height - 10)  # Adjust font size to fit
            rendered_text = font.render(option, True, color)
            text_rect = rendered_text.get_rect(center=rect.center)
            self.window.blit(rendered_text, text_rect)
            self.button_rects.append((rect, option))


    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    mouse_pos = event.pos
                    for i, (rect, option) in enumerate(self.button_rects):
                        if rect.collidepoint(mouse_pos):
                            if not self.showing_special_attacks:
                                if option == "Attack":
                                    return "basic_attack"
                                elif option == "Special Attacks":
                                    self.showing_special_attacks = True
                                    self.selected_attack = 0
                                    return None
                                elif option == "Use Items":
                                    return "use_item"
                                elif option == "Run":
                                    return "run"
                            else:
                                return i
        return None


    def player_attack(self):
        selected_option = self.handle_events()
        if selected_option is not None:
            if selected_option == "basic_attack":
                damage = self.player.basic_attack(self.enemy)
                print("Player uses basic attack! Deals damage to the enemy.")
                if self.enemy.get_hit_points() <= 0:
                    print("Enemy defeated!")
                    return 'enemy_defeated'
                self.player_turn = False
                return 'player_attacked'
            elif selected_option == "use_item":
                print("Using item (not yet implemented).")
                # Implement item usage here
            elif selected_option == "run":
                print("Running away (not yet implemented).")
                # Implement running away here
            else:  # Special attack
                attack_list = list(self.player.get_attacks().keys())
                attack_name = attack_list[selected_option]
                damage = self.player.get_attacks()[attack_name]["method"](self.enemy)
                print(f"Player uses {attack_name}! Deals damage to the enemy.")
                if self.enemy.get_hit_points() <= 0:
                    print("Enemy defeated!")
                    return 'enemy_defeated'
                self.player_turn = False
                return 'player_attacked'
        return 'not_player_turn'


    def enemy_attack(self):
        if not self.player_turn:
            damage = self.enemy.attack(self.player)
            if self.player.get_hit_points() <= 0:
                print("Player defeated!")
                return 'player_defeated'
            self.player_turn = True
            return 'enemy_attacked'
        return 'not_enemy_turn'

    def find_font_size(self, text, max_width, max_height):
        font_size = 36
        font = pygame.font.Font(self.font_path, font_size)
        text_width, text_height = font.size(text)
        while text_width > max_width or text_height > max_height:
            font_size -= 1
            font = pygame.font.Font(self.font_path, font_size)
            text_width, text_height = font.size(text)
        return font
