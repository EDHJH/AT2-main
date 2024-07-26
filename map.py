import pygame, random, time
from assets import GAME_ASSETS
from Enemies.enemy import Enemy
from Enemies.boss import Boss
from Characters.necromancer import Necromancer
from Characters.warrior import Warrior
from Characters.ranger import Ranger
from turnbase import Turnbased  # Import the Turnbased class

class Map:
    def __init__(self, window):
        self.window = window
        self.map_image = pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
        self.new_map_image = pygame.image.load(GAME_ASSETS["dungeon_map1"]).convert_alpha()  # Load the new map image
        self.new_map_image = pygame.transform.scale(self.new_map_image, (self.window.get_width(), self.window.get_height()))
        self.player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Necromancer': pygame.image.load(GAME_ASSETS["necromancer"]).convert_alpha(),
            'Ranger': pygame.image.load(GAME_ASSETS['ranger']).convert_alpha()
        }
        self.player_type = None
        self.player_position = [self.window.get_width() / 2, self.window.get_height() / 2]
        self.enemies = [
            Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
            Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
            Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window)
        ]
        self.in_combat = False
        self.current_enemy = None
        self.game_over = False

        # Font
        self.font_path = "assets/slkscre.ttf"
        self.font = pygame.font.Font(self.font_path, 20)

        # Create a player instance
        self.player = None
        self.turn_based_combat = None  # Initialize the turn-based combat system

        # Run Time
        self.last_run_time = 0  # Track the time when the character last ran from combat
        self.run_cooldown = 2  # Cooldown period in seconds

        # Stats button
        self.stats_button_rect = pygame.Rect(self.window.get_width() // 2 - 50, 10, 100, 50)
        self.show_stats = False
        self.last_stats_toggle = 0  # To handle the toggle delay
        self.stats_toggle_delay = 0.2  # 200 milliseconds delay
        
        self.player_level = 1  # Initialize player level
        self.level_up_options = False
        self.boss_spawned = False

        # NPC AT END
        self.npc_image = pygame.image.load(GAME_ASSETS["npc"]).convert_alpha()
        self.npc_displayed = False
        self.congratulatory_message = "Thank you for killing the boss!\nThe Crystal of the Eternal Light is now back to us,\nthe world is full of light and hope again!"


    def load_player(self, character_type):
        self.player_type = character_type
        self.player_image = self.player_images[character_type]
        # Scale the player image to be larger (e.g., 1.5 times its original size)
        scale_factor = 0.4
        self.player_image = pygame.transform.scale(self.player_image, 
                        (int(self.player_image.get_width() * scale_factor), 
                        int(self.player_image.get_height() * scale_factor)))
        if character_type == "Necromancer":
            self.player = Necromancer("Player", 100)  # Create a Necromancer player with 100 HP
        elif character_type == "Warrior":
            self.player = Warrior("Player", 150)  # Create a Warrior player with 150 HP
        elif character_type == "Ranger":
            self.player = Ranger("Player", 120)  # Create a Ranger player with 120 HP

    def check_for_combat(self):
        current_time = time.time()
        if current_time - self.last_run_time < self.run_cooldown:
            return False  # Skip combat if within cooldown period

        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False
    
    def spawn_boss(self):
        self.boss = Boss(GAME_ASSETS["boss"], [self.window.get_width() / 2, self.window.get_height() / 2], self.window)
        self.enemies.append(self.boss)
        print("Boss has spawned!")

    def reload_mobs(self):
        # Define base stats for each enemy
        base_stats = {
            "goblin": {"hp": 50, "damage": 10, "armor": 5},
            "orc": {"hp": 80, "damage": 15, "armor": 10},
            "skeleton": {"hp": 60, "damage": 12, "armor": 8},
        }

        # Check if the player's level is 5 or higher
        if self.player.get_level() >= 5:
            for key in base_stats:
                base_stats[key]["hp"] *= 3
                base_stats[key]["damage"] *= 2
                base_stats[key]["armor"] *= 2

        self.enemies = [
            Enemy(GAME_ASSETS["skeleton"], [60, 200], self.window, **base_stats["skeleton"]),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 320, 70], self.window, **base_stats["orc"]),
            Enemy(GAME_ASSETS["goblin"], [90, self.window.get_height() - 200], self.window, **base_stats["goblin"]),
            Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() - 400, self.window.get_height() - 210], self.window, **base_stats["skeleton"])
        ]

    def handle_combat(self):
        if self.in_combat and self.turn_based_combat:
            if self.turn_based_combat.player_turn:
                result = self.turn_based_combat.player_attack()
                if result == 'enemy_defeated':
                    self.enemies.remove(self.current_enemy)
                    self.in_combat = False
                    self.turn_based_combat = None
                    self.current_enemy = None
                    self.player.level_up()  # Level up the player after defeating an enemy
                    self.player.increase_max_hp(10)
                    self.player.increase_max_stamina(20)
                    self.player.increase_strength(1)
                    if self.player.get_level() == 5:
                        self.map_image = pygame.image.load(GAME_ASSETS["dungeon_map1"]).convert_alpha()
                        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
                        self.reload_mobs()  # Reload the mobs
                else:
                    result = self.turn_based_combat.enemy_attack()
                    if result == 'player_defeated':
                        self.game_over = True


    def handle_events(self):
        if self.game_over:
            return 'quit'

        keys = pygame.key.get_pressed()
        move_speed = 8  # Set a consistent movement speed for the player

        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if self.stats_button_rect.collidepoint(mouse_pos) and current_time - self.last_stats_toggle > self.stats_toggle_delay:
                        self.show_stats = not self.show_stats  # Toggle stats display
                        self.last_stats_toggle = current_time

        if not self.in_combat:
            # Movement
            if keys[pygame.K_a] and self.player_position[0] > 0:  # Move left if 'a' is pressed and within boundary
                self.player_position[0] -= move_speed
            if keys[pygame.K_d] and self.player_position[0] < self.window.get_width() - self.player_image.get_width():  # Move right if 'd' is pressed and within boundary
                self.player_position[0] += move_speed
            if keys[pygame.K_w] and self.player_position[1] > 0:  # Move up if 'w' is pressed and within boundary
                self.player_position[1] -= move_speed
            if keys[pygame.K_s] and self.player_position[1] < self.window.get_height() - self.player_image.get_height():  # Move down if 's' is pressed and within boundary
                self.player_position[1] += move_speed
            # Stats
            if keys[pygame.K_e] and current_time - self.last_stats_toggle > self.stats_toggle_delay:  # Press 'e' to toggle stats
                self.show_stats = not self.show_stats  # Toggle stats display
                self.last_stats_toggle = current_time

        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()
        
        # Check if player is level 10 and boss is defeated
        if self.player.get_level() == 10 and not self.npc_displayed:
            self.npc_displayed = True

        self.draw()

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
        font = pygame.font.Font(self.font_path, 20)  # Use the same font path and size as turn-based combat
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

    def draw_stats_screen(self):
        # Background rectangle
        stats_rect = pygame.Rect(self.window.get_width() // 2 - 250, self.window.get_height() // 2 - 150, 500, 350)
        stats_surface = pygame.Surface(stats_rect.size, pygame.SRCALPHA)
        stats_surface.fill((0, 0, 0, 128))  # Half-transparent black
        self.window.blit(stats_surface, stats_rect.topleft)

        # White border around the stats screen
        pygame.draw.rect(self.window, (255, 255, 255), stats_rect, 2)

        font = pygame.font.Font(self.font_path, 24)

        stats_texts = [
            f"Health: {self.player.get_current_hp()}",
            f"Strength: {self.player.get_strength()}",
            f"Stamina: {self.player.get_current_stamina()}",
            f"Defense: {self.player.get_armor()}",
            f"Level: {self.player.get_level()}"  # Display the current level
        ]

        y_offset = stats_rect.top + 10
        for text in stats_texts:
            text_surface = font.render(text, True, (255, 255, 255))
            self.window.blit(text_surface, (stats_rect.left + 10, y_offset))
            y_offset += 30

        # Space between stats and special attacks
        y_offset += 10

        # Special attacks title
        special_attacks_title = font.render("Special Attacks:", True, (255, 255, 255))
        self.window.blit(special_attacks_title, (stats_rect.left + 10, y_offset))
        y_offset += 30

        # Special attacks with their stamina costs
        for attack, info in self.player.get_attacks().items():
            text_surface = font.render(f"{attack}: {info['stamina_cost']} stamina", True, (255, 255, 255))
            self.window.blit(text_surface, (stats_rect.left + 10, y_offset))
            y_offset += 30
    
    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))
        for enemy in self.enemies:
            enemy.draw()

        # Draw player health bar on the top left corner
        self.draw_health_bar(self.player, 10, 10, 200, 20)
        
        # Draw player stamina bar below the health bar
        self.draw_stamina_bar(self.player, 10, 40, 200, 20)

        # Draw stats button
        mouse_pos = pygame.mouse.get_pos()
        font = pygame.font.Font(self.font_path, 24)
        if self.stats_button_rect.collidepoint(mouse_pos):
            text_surface = font.render("Stats (e)", True, (0, 0, 255))  # Blue text when hovered
        else:
            text_surface = font.render("Stats (e)", True, (255, 255, 255))  # White text

        text_rect = text_surface.get_rect(center=self.stats_button_rect.center)
        self.window.blit(text_surface, text_rect)

        if self.show_stats:
            self.draw_stats_screen()

        # Check if NPC should be displayed
        if self.npc_displayed:
            npc_position = (self.window.get_width() // 2 - self.npc_image.get_width() // 2, self.window.get_height() // 2 - self.npc_image.get_height() // 2 + 50)
            
            # Display the congratulatory message with a half-transparent background
            message_font = pygame.font.Font(self.font_path, 24)
            lines = [
                "Thank you for killing the boss!",
                "The Crystal of the Eternal Light is now back to us,",
                "the world is full of light and hope again!"
            ]
            message_surfaces = [message_font.render(line, True, (255, 255, 255)) for line in lines]
            
            # Determine the total height of the message block
            total_height = sum(surface.get_height() for surface in message_surfaces) + (len(message_surfaces) - 1) * 10
            
            # Calculate the position for the background and text above the NPC
            background_rect = pygame.Rect(npc_position[0] - 150, npc_position[1] - total_height - 30, self.npc_image.get_width() + 300, total_height + 60)
            background_surface = pygame.Surface(background_rect.size, pygame.SRCALPHA)
            background_surface.fill((0, 0, 0, 128))  # Half-transparent black
            self.window.blit(background_surface, background_rect.topleft)
            
            # Draw the white border around the background
            pygame.draw.rect(self.window, (255, 255, 255), background_rect, 2)
            
            # Draw the message text centered within the background
            y_offset = background_rect.top + 15
            for surface in message_surfaces:
                text_rect = surface.get_rect(center=(background_rect.centerx, y_offset + surface.get_height() // 2))
                self.window.blit(surface, text_rect.topleft)
                y_offset += surface.get_height() + 10

            # Draw the NPC image
            self.window.blit(self.npc_image, npc_position)

            # Draw the Quit button
            quit_button_rect = pygame.Rect(self.window.get_width() // 2 - 50, self.window.get_height() - 60, 100, 40)
            pygame.draw.rect(self.window, (255, 255, 255), quit_button_rect, 2)
            quit_text = font.render("Quit", True, (255, 255, 255))
            quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
            self.window.blit(quit_text, quit_text_rect)
            
            # Check for quit button click
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if quit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            exit()

        pygame.display.flip()

    def update(self):
        if not self.enemies and not self.in_combat:
            self.map_image = self.new_map_image  # Switch to the new map if no enemies and not in combat