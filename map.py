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

        # Create a player instance
        self.player = None
        self.turn_based_combat = None  # Initialize the turn-based combat system

        # Run Time
        self.last_run_time = 0  # Track the time when the character last ran from combat
        self.run_cooldown = 2  # Cooldown period in seconds

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
            else:
                result = self.turn_based_combat.enemy_attack()
                if result == 'player_defeated':
                    self.game_over = True

    def handle_events(self):
        if self.game_over:
            return 'quit'

        keys = pygame.key.get_pressed()
        move_speed = 5  # Set a consistent movement speed for the player

        if keys[pygame.K_a] and not keys[pygame.K_d]:  # Move left if 'a' is pressed and 'd' is not pressed
            self.player_position[0] -= move_speed
        elif keys[pygame.K_d] and not keys[pygame.K_a]:  # Move right if 'd' is pressed and 'a' is not pressed
            self.player_position[0] += move_speed
        elif keys[pygame.K_w] and not keys[pygame.K_s]:  # Move up if 'w' is pressed and 's' is not pressed
            self.player_position[1] -= move_speed
        elif keys[pygame.K_s] and not keys[pygame.K_w]:  # Move down if 's' is pressed and 'w' is not pressed
            self.player_position[1] += move_speed

        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()
    
    def draw_health_bar(self, entity, x, y, width, height):
    # Calculate health percentage
        health_percentage = entity.get_current_hp() / entity.get_max_hp()

        # Calculate the width of the health bar
        health_bar_width = int(width * health_percentage)

        # Draw the health bar background
        pygame.draw.rect(self.window, (255, 0, 0), (x, y, width, height))  # Red background

        # Draw the current health
        pygame.draw.rect(self.window, (0, 255, 0), (x, y, health_bar_width, height))  # Green health


    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))
        for enemy in self.enemies:
            enemy.draw()

        # Draw player health bar on the top left corner
        self.draw_health_bar(self.player, 10, 10, 200, 20)

        pygame.display.flip()

