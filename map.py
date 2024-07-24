import random
import pygame
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
        self.blue_orb = None
        self.game_over = False

        # Create a player instance
        self.player = None
        self.turn_based_combat = None  # Initialize the turn-based combat system

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
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:
                self.in_combat = True
                self.current_enemy = enemy
                self.turn_based_combat = Turnbased(self.player, self.current_enemy, self.window)  # Initialize turn-based combat
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

    def spawn_blue_orb(self):
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            self.game_over = True
            print("YOU WIN")
            return True
        return False

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

        if self.blue_orb and self.check_orb_collision():
            return 'quit'

    def draw_health_bar(self):
        if self.player is None:
            return
        bar_width = 200
        bar_height = 20
        health_ratio = self.player.get_current_hp() / self.player.get_max_hp()
        health_bar_width = int(bar_width * health_ratio)
        pygame.draw.rect(self.window, (255, 0, 0), (10, 10, bar_width, bar_height))
        pygame.draw.rect(self.window, (0, 255, 0), (10, 10, health_bar_width, bar_height))

    def draw(self):
        self.window.fill((0, 0, 0))
        if self.in_combat:
            self.turn_based_combat.draw_combat_ui()  # Draw the turn-based combat UI
        else:
            self.window.blit(self.map_image, (0, 0))
            self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))
            for enemy in self.enemies:
                enemy.draw()
            if self.blue_orb:
                self.window.blit(self.blue_orb, self.orb_position)

            # Draw health bar
            self.draw_health_bar()

            pygame.display.flip()
