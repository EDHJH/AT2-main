# map.py
import pygame
import random
from enemy import Enemy
from goblin import Goblin
from orc import Orc
from skeleton import Skeleton
from assets import GAME_ASSETS

class Map:
    def __init__(self, window):
        self.__window = window
        self.__map_image = pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha()
        self.__map_image = pygame.transform.scale(self.__map_image, (self.__window.get_width(), self.__window.get_height()))
        self.__player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Rogue': pygame.image.load(GAME_ASSETS["rogue"]).convert_alpha()
        }
        self.__player_type = None
        self.__player_position = [self.__window.get_width() / 2, self.__window.get_height() / 2]
        self.__enemies = [
            Goblin([10, 10], self.__window),
            Orc([self.__window.get_width() - 120, 50], self.__window),
            Skeleton([50, self.__window.get_height() - 120], self.__window),
            Skeleton([self.__window.get_width() - 120, self.__window.get_height() - 120], self.__window)
        ]
        self.__in_combat = False
        self.__current_enemy = None
        self.__blue_orb = None
        self.__game_over = False

    def load_player(self, character_type):
        self.__player_type = character_type
        self.__player_image = self.__player_images[character_type]
        self.__player_image = pygame.transform.scale(self.__player_image, (int(self.__player_image.get_width() * 0.15), int(self.__player_image.get_height() * 0.15)))

    def check_for_combat(self):
        for enemy in self.__enemies:
            if pygame.math.Vector2(enemy.get_position()).distance_to(self.__player_position) < 50:
                self.__in_combat = True
                self.__current_enemy = enemy
                return True
        return False

    def handle_combat(self):
        if self.__in_combat and self.__current_enemy:
            player_damage = random.randint(5, 10)
            enemy_defeated = self.__current_enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")
            if enemy_defeated:
                print("Enemy defeated!")
                self.__enemies.remove(self.__current_enemy)
                self.__in_combat = False
                self.__current_enemy = None
                if not self.__enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(5, 10)
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                # Assume player has a method to take damage
                # self.player.take_damage(enemy_damage)

    def spawn_blue_orb(self):
        self.__blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.__blue_orb = pygame.transform.scale(self.__blue_orb, (50, 50))
        self.__orb_position = [self.__window.get_width() / 2 - 25, self.__window.get_height() / 2 - 25]

    def check_orb_collision(self):
        if self.__blue_orb and pygame.math.Vector2(self.__orb_position).distance_to(self.__player_position) < 25:
            self.__game_over = True
            print("YOU WIN")  # This can be modified to a more visual display if needed.
            return True
        return False

    def handle_events(self):
        if self.__game_over:
            return 'quit'  # Stop processing events if game is over

        keys = pygame.key.get_pressed()
        move_speed = 2
        if keys[pygame.K_LEFT]:
            self.__player_position[0] -= move_speed
        if keys[pygame.K_RIGHT]:
            self.__player_position[0] += move_speed
        if keys[pygame.K_UP]:
            self.__player_position[1] -= move_speed
        if keys[pygame.K_DOWN]:
            self.__player_position[1] += move_speed

        if not self.__in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()

        if self.__blue_orb and self.check_orb_collision():
            return 'quit'

    def draw(self):
        self.__window.fill((0, 0, 0))
        self.__window.blit(self.__map_image, (0, 0))
        self.__window.blit(self.__player_image, (self.__player_position[0], self.__player_position[1]))
        for enemy in self.__enemies:
            enemy.draw()
        if self.__blue_orb:
            self.__window.blit(self.__blue_orb, self.__orb_position)
        pygame.display.flip()

    # Getter and Setter methods
    def get_window(self):
        return self.__window

    def set_window(self, window):
        self.__window = window

    def get_map_image(self):
        return self.__map_image

    def set_map_image(self, map_image):
        self.__map_image = map_image

    def get_player_images(self):
        return self.__player_images

    def set_player_images(self, player_images):
        self.__player_images = player_images

    def get_player_type(self):
        return self.__player_type

    def set_player_type(self, player_type):
        self.__player_type = player_type

    def get_player_position(self):
        return self.__player_position

    def set_player_position(self, player_position):
        self.__player_position = player_position

    def get_enemies(self):
        return self.__enemies

    def set_enemies(self, enemies):
        self.__enemies = enemies

    def get_in_combat(self):
        return self.__in_combat

    def set_in_combat(self, in_combat):
        self.__in_combat = in_combat

    def get_current_enemy(self):
        return self.__current_enemy

    def set_current_enemy(self, current_enemy):
        self.__current_enemy = current_enemy

    def get_blue_orb(self):
        return self.__blue_orb

    def set_blue_orb(self, blue_orb):
        self.__blue_orb = blue_orb

    def get_game_over(self):
        return self.__game_over

    def set_game_over(self, game_over):
        self.__game_over = game_over
