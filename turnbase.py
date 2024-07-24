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
        self.font = pygame.font.Font(None, 36)  # Font for rendering text
        self.selected_attack = 0

        # Load player image
        self.player_image = pygame.image.load(GAME_ASSETS[f"{self.player.get_character_class().lower()}"]).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.75), int(self.player_image.get_height() * 0.75)))

        # Load enemy image
        enemy_image_path = self.enemy.get_image_path()
        self.enemy_image = pygame.image.load(enemy_image_path).convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (int(self.enemy_image.get_width() * 0.75), int(self.enemy_image.get_height() * 0.75)))

    def draw_combat_ui(self):
        self.window.blit(self.turn_background_image, (0, 0))
        self.window.blit(self.panel_image, (0, self.window.get_height() - 150))  # Position the panel at the bottom

        # Draw player and enemy
        player_pos = (self.window.get_width() * 0.25 - self.player_image.get_width() // 2, self.window.get_height() * 0.5 - self.player_image.get_height() // 2)
        enemy_pos = (self.window.get_width() * 0.75 - self.enemy_image.get_width() // 2, self.window.get_height() * 0.5 - self.enemy_image.get_height() // 2)
        self.window.blit(self.player_image, player_pos)
        self.window.blit(self.enemy_image, enemy_pos)

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
            rendered_text = self.font.render(text, True, (255, 255, 255))
            self.window.blit(rendered_text, (20, panel_top + 20 + i * 30))

    def draw_attack_options(self):
        panel_top = self.window.get_height() - 150
        # Draw attack options on top of the panel
        attacks = self.player.get_attacks()
        attack_list = list(attacks.items())

        for i, (attack, info) in enumerate(attack_list):
            color = (255, 0, 0) if i == self.selected_attack else (255, 255, 255)
            text = f"{i + 1}. {attack} (Stamina: {info['stamina_cost']})"
            rendered_text = self.font.render(text, True, color)
            self.window.blit(rendered_text, (self.window.get_width() // 2 + 20, panel_top + 20 + i * 30))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_attack = (self.selected_attack - 1) % len(self.player.get_attacks())
                elif event.key == pygame.K_DOWN:
                    self.selected_attack = (self.selected_attack + 1) % len(self.player.get_attacks())
                elif event.key == pygame.K_RETURN:
                    return self.selected_attack
        return None

    def player_attack(self):
        selected_attack = self.handle_events(pygame.event.get())
        if selected_attack is not None:
            attack_list = list(self.player.get_attacks().items())
            attack, attack_info = attack_list[selected_attack]
            if self.player.get_current_stamina() >= attack_info["stamina_cost"]:
                self.player.choose_attack(self.enemy)
                print(f"Player attacks with {attack}! Deals damage to the enemy.")
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
