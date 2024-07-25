import pygame, random, time
from assets import GAME_ASSETS
from Enemies.enemy import Enemy
from Characters.necromancer import Necromancer
from Characters.warrior import Warrior
from Characters.ranger import Ranger
from turnbase import Turnbased  # Import the Turnbased class

class Map:
    def __init__(self, window):
        self.window = window
        self.map_image = pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
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



    def load_player(self, character_type):
        self.player_type = character_type
        self.player_image = self.player_images[character_type]
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.15), int(self.player_image.get_height() * 0.15)))
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

    def handle_combat(self):
        if self.in_combat and self.turn_based_combat:
            if self.turn_based_combat.player_turn:
                result = self.turn_based_combat.player_attack()
                if result == 'enemy_defeated':
                    self.enemies.remove(self.current_enemy)
                    self.in_combat = False
                    self.turn_based_combat = None
                    self.current_enemy = None
                    if not self.enemies:
                        self.spawn_blue_orb()
            else:
                result = self.turn_based_combat.enemy_attack()
                if result == 'player_defeated':
                    self.game_over = True

    def handle_events(self):
        if self.game_over:
            return 'quit'

        keys = pygame.key.get_pressed()
        move_speed = 5  # Set a consistent movement speed for the player

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
        stats_rect = pygame.Rect(self.window.get_width() // 2 - 250, self.window.get_height() // 2 - 150, 500, 300)
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
            f"Defense: {self.player.get_armor()}"
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

        pygame.display.flip()
