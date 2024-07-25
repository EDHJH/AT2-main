import pygame, random
from assets import GAME_ASSETS

class Turnbased:
    def __init__(self, player, enemy, window):
        self.player = player
        self.enemy = enemy
        self.window = window
        self.player_turn = True
        self.round_counter = 0  # Initialize round counter
        self.turn_background_image = pygame.image.load(GAME_ASSETS["lv1_turn_background"]).convert()
        self.turn_background_image = pygame.transform.scale(self.turn_background_image, (self.window.get_width(), self.window.get_height()))
        self.panel_image = pygame.image.load(GAME_ASSETS["panel"]).convert_alpha()
        self.panel_image = pygame.transform.scale(self.panel_image, (self.window.get_width(), 150))  # Adjust the height as needed
        self.ground_image = pygame.image.load(GAME_ASSETS["ground"]).convert()
        self.ground_image_width, self.ground_image_height = self.ground_image.get_size()

        # Load the custom font
        self.font_path = "assets/slkscre.ttf"  # Path to the TTF file
        self.font_stats = pygame.font.Font(self.font_path, 36)  # Default font for player stats
        self.font_log = pygame.font.Font(self.font_path, 14)  # Smaller font for logs

        self.selected_attack = 0
        self.showing_special_attacks = False
        self.action_log = []  # To store the logs of actions

        # Potions
        self.showing_items = False
        self.health_potions = 3
        self.stamina_potions = 3

        # Load player image
        self.player_image = pygame.image.load(GAME_ASSETS[f"{self.player.get_character_class().lower()}"]).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.75), int(self.player_image.get_height() * 0.75)))

        # Load enemy image
        enemy_image_path = self.enemy.get_image_path()
        self.enemy_image = pygame.image.load(enemy_image_path).convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (int(self.enemy_image.get_width() * 0.75), int(self.enemy_image.get_height() * 0.75)))

        # Dead Screen
        self.dead_screen_image = pygame.image.load(GAME_ASSETS["dead_screen"]).convert_alpha()
        self.dead_screen_image = pygame.transform.scale(self.dead_screen_image, (self.window.get_width(), self.window.get_height()))

    def draw_health_bar(self, entity, x, y, width, height):
    # Calculate health percentage
        health_percentage = entity.get_current_hp() / entity.get_max_hp()

        # Calculate the width of the health bar
        health_bar_width = int(width * health_percentage)

        # Draw the health bar background (red for missing health)
        pygame.draw.rect(self.window, (255, 0, 0), (x, y, width, height))  # Red background

        # Draw the current health (green)
        pygame.draw.rect(self.window, (0, 255, 0), (x, y, health_bar_width, height))  # Green health

        # Draw black border around the health bar
        pygame.draw.rect(self.window, (0, 0, 0), (x, y, width, height), 2)  # Black border

        # Draw current health as black numbers inside the bar
        health_text = f"{entity.get_current_hp()}/{entity.get_max_hp()}"
        font = pygame.font.Font(self.font_path, 20)  # Adjust font size as needed
        text_surface = font.render(health_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.window.blit(text_surface, text_rect)

    def draw_stamina_bar(self, entity, x, y, width, height):
        # Calculate stamina percentage
        stamina_percentage = entity.get_current_stamina() / entity.get_max_stamina()

        # Calculate the width of the stamina bar
        stamina_bar_width = int(width * stamina_percentage)

        # Draw the stamina bar background (gray for missing stamina)
        pygame.draw.rect(self.window, (169, 169, 169), (x, y, width, height))  # Gray background

        # Draw the current stamina (blue)
        pygame.draw.rect(self.window, (0, 0, 255), (x, y, stamina_bar_width, height))  # Blue stamina

        # Draw black border around the stamina bar
        pygame.draw.rect(self.window, (0, 0, 0), (x, y, width, height), 2)  # Black border

        # Draw current stamina as black numbers inside the bar
        stamina_text = f"{entity.get_current_stamina()}/{entity.get_max_stamina()}"
        font = pygame.font.Font(self.font_path, 20)  # Use the same font path and size as turn-based combat
        text_surface = font.render(stamina_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.window.blit(text_surface, text_rect)

    def use_health_potion(self):
        if self.health_potions > 0:
            self.player.heal(30)
            self.health_potions -= 1
            self.action_log.append("Used a health potion. Restored 30 HP.")
        else:
            self.action_log.append("No health potions left!")
    
    def use_stamina_potion(self):
        if self.stamina_potions > 0:
            self.player.regenerate_stamina(full=True)
            self.stamina_potions -= 1
            self.action_log.append("Used a stamina potion. Restored 50 stamina.")
        else:
            self.action_log.append("No stamina potions left!")

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

        # Draw player health bar in the top left corner
        self.draw_health_bar(self.player, 10, 10, 200, 20)
        
        # Draw player stamina bar below the health bar
        self.draw_stamina_bar(self.player, 10, 40, 200, 20)

        # Draw enemy health bar in the top right corner
        self.draw_health_bar(self.enemy, self.window.get_width() - 210, 10, 200, 20)

        # Draw attack options on the panel
        self.draw_attack_options()

        # Draw battle log on the left side of the panel
        self.draw_action_log()

        pygame.display.flip()

    def draw_attack_options(self):
        panel_top = self.window.get_height() - 150

        if self.showing_items:
            options = [f"Health Potion ({self.health_potions})", f"Stamina Potion ({self.stamina_potions})", "Back"]
        elif not self.showing_special_attacks:
            options = ["Attack", "Special Attacks", "Use Items", "Run"]
        else:
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

    def draw_action_log(self):
        panel_top = self.window.get_height() - 150
        log_x = 20
        log_y = panel_top + 20
        log_height = 100
        log_width = self.window.get_width() // 2 - 40

        for i, log in enumerate(self.action_log[-3:]):  # Show last 3 actions
            rendered_text = self.font_log.render(log, True, (255, 255, 255))
            self.window.blit(rendered_text, (log_x, log_y + i * 30))

    def regenerate_stamina(self):
        self.player.regenerate_stamina()
        log = f"Player regenerates {self.player.get_stamina_regeneration()} stamina."
        self.action_log.append(log)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    mouse_pos = event.pos
                    for i, (rect, option) in enumerate(self.button_rects):
                        if rect.collidepoint(mouse_pos):
                            if self.showing_items:
                                if option.startswith("Health Potion"):
                                    self.use_health_potion()
                                    self.showing_items = False
                                    return 'item_used'
                                elif option.startswith("Stamina Potion"):
                                    self.use_stamina_potion()
                                    self.showing_items = False
                                    return 'item_used'
                                elif option == "Back":
                                    self.showing_items = False
                                    return None
                            elif not self.showing_special_attacks:
                                if option == "Attack":
                                    return "basic_attack"
                                elif option == "Special Attacks":
                                    if self.player.get_current_stamina() >= min([info['stamina_cost'] for info in self.player.get_attacks().values()]):
                                        self.showing_special_attacks = True
                                        self.selected_attack = 0
                                    else:
                                        self.action_log.append("Not enough stamina to use any special attacks!")
                                    return None
                                elif option == "Use Items":
                                    self.showing_items = True
                                    self.selected_attack = 0
                                    return None
                                elif option == "Run":
                                    return "run"
                            else:
                                return i  # Return the index for special attacks
        return None

    def player_attack(self):
        selected_option = self.handle_events()
        if selected_option is not None:
            if selected_option == "basic_attack":
                damage = self.player.basic_attack(self.enemy)
                log = f"Player uses basic attack! Deals {damage} damage to the enemy."
                self.action_log.append(log)
                if self.enemy.get_hit_points() <= 0:
                    log = "Enemy defeated!"
                    self.action_log.append(log)
                    self.showing_special_attacks = False  # Reset to main attack options
                    self.round_counter = 0  # Reset round counter
                    return 'enemy_defeated'
                self.player_turn = False
                self.showing_special_attacks = False  # Reset to main attack options
                self.round_counter += 1
                if self.round_counter % 2 == 0:
                    self.regenerate_stamina()
                return 'player_attacked'
            elif selected_option == "use_item":
                log = "Using item (not yet implemented)."
                self.action_log.append(log)
                # Implement item usage here
            elif selected_option == "run":
                run_successful = random.randint(0, 10) > 5
                if run_successful:
                    log = "Run successful! Exiting combat."
                    self.action_log.append(log)
                    self.showing_special_attacks = False  # Reset to main attack options
                    self.round_counter = 0  # Reset round counter
                    return 'run_successful'
                else:
                    log = "Run failed! Enemy attacks."
                    self.action_log.append(log)
                    self.player_turn = False
                    self.round_counter += 1
                    if self.round_counter % 2 == 0:
                        self.regenerate_stamina()
                    return 'run_failed'
            else:  # Special attack
                attack_list = list(self.player.get_attacks().keys())
                # Ensure selected_option is an index here
                if isinstance(selected_option, str):
                    try:
                        selected_option = int(selected_option)
                    except ValueError:
                        return 'not_player_turn'

                attack_name = attack_list[selected_option]
                attack_info = self.player.get_attacks()[attack_name]
                if self.player.get_current_stamina() >= attack_info["stamina_cost"]:
                    damage = attack_info["method"](self.enemy)
                    self.player.consume_stamina(attack_info["stamina_cost"])
                    log = f"Player uses {attack_name}! Deals {damage} damage to the enemy."
                    self.action_log.append(log)
                    if self.enemy.get_hit_points() <= 0:
                        log = "Enemy defeated!"
                        self.action_log.append(log)
                        self.showing_special_attacks = False  # Reset to main attack options
                        self.round_counter = 0  # Reset round counter
                        return 'enemy_defeated'
                    self.player_turn = False
                    self.showing_special_attacks = False  # Reset to main attack options
                    self.round_counter += 1
                    if self.round_counter % 2 == 0:
                        self.regenerate_stamina()
                    return 'player_attacked'
                else:
                    log = f"Not enough stamina to use {attack_name}!"
                    self.action_log.append(log)
        if self.player.get_current_hp() <= 0:
            result = self.display_dead_screen()
            if result == 'main_menu':
                return 'main_menu'
        return 'not_player_turn'

    def enemy_attack(self):
        if not self.player_turn:
            damage = self.enemy.attack(self.player)
            log = f"Enemy attacks! Deals {damage} damage to the player."
            self.action_log.append(log)
            if self.player.get_hit_points() <= 0:
                log = "Player defeated!"
                self.action_log.append(log)
                self.showing_special_attacks = False  # Reset to main attack options
                result = self.display_dead_screen()  # Display the dead screen
                if result == 'main_menu':
                    return 'main_menu'
                return 'player_defeated'
            self.player_turn = True
            self.showing_special_attacks = False  # Reset to main attack options
            self.round_counter += 1
            if self.round_counter % 2 == 0:
                self.regenerate_stamina()
            return 'enemy_attacked'
        return 'not_enemy_turn'



    def display_dead_screen(self):
        self.window.blit(self.dead_screen_image, (0, 0))
        
        # Draw quit button
        button_width = 250
        button_height = 60
        padding_y = 20

        quit_rect = pygame.Rect(self.window.get_width() // 2 - button_width // 2, self.window.get_height() - button_height - padding_y, button_width, button_height)

        pygame.draw.rect(self.window, (255, 255, 255), quit_rect, 2)

        font = self.find_font_size("Quit", button_width - 10, button_height - 10)
        quit_text = font.render("Quit", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        self.window.blit(quit_text, quit_text_rect)

        self.button_rects = [(quit_rect, "Quit")]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        mouse_pos = event.pos
                        for rect, option in self.button_rects:
                            if rect.collidepoint(mouse_pos) and option == "Quit":
                                pygame.quit()
                                exit()

    def find_font_size(self, text, max_width, max_height):
        font_size = 36
        font = pygame.font.Font(self.font_path, font_size)
        text_width, text_height = font.size(text)
        while text_width > max_width or text_height > max_height:
            font_size -= 1
            font = pygame.font.Font(self.font_path, font_size)
            text_width, text_height = font.size(text)
        return font
