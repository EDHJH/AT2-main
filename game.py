import pygame, time
from menu import MainMenu
from Characters.character_select import CharacterSelect
from map import Map
from assets import load_assets, GAME_ASSETS
from turnbase import Turnbased

class Game:
    def __init__(self):
        pygame.init()
        load_assets()  # Load the game image assets
        self.window = pygame.display.set_mode((1280, 720))
        self.menu = MainMenu(self.window)  # Create an instance of the MainMenu class
        self.character_select = CharacterSelect(self.window)  # Create an instance of the CharacterSelect class
        self.game_map = Map(self.window)  # Create an instance of the Map class
        self.state = 'menu'  # Set the initial state to 'menu'
        self.current_character = None  # To store the chosen character
        self.turnbased = None  # Initialize turnbased combat placeholder

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    return

            if self.state == 'menu':
                result = self.menu.handle_events(events)
                if result == 'Start Game':
                    self.state = 'character_select'
                    pass
                elif result == 'Exit':
                    pygame.quit()
                    running = False
                    return
                self.menu.draw()

            elif self.state == 'character_select':
                selected_character = self.character_select.run()
                if selected_character == 'back':
                    self.state = 'menu'
                elif selected_character:
                    self.current_character = selected_character
                    self.game_map.load_player(selected_character)
                    self.state = 'game_map'

            elif self.state == 'game_map':
                result = self.game_map.handle_events()
                if result == 'back':
                    self.state = 'character_select'
                elif result == 'quit':
                    pygame.quit()
                    running = False
                    return
                else:
                    self.game_map.draw()
                # Check for combat state
                if self.game_map.in_combat:
                    self.state = 'combat'
                    self.turnbased = Turnbased(self.game_map.player, self.game_map.current_enemy, self.window)

            elif self.state == 'combat':
                self.turnbased.draw_combat_ui()

                if self.turnbased.player_turn:
                    result = self.turnbased.player_attack()
                    if result == 'enemy_defeated':
                        print("You won the combat!")
                        self.game_map.enemies.remove(self.game_map.current_enemy)
                        self.game_map.player.level_up()  # Level up the player after defeating an enemy
                        self.game_map.player.increase_max_hp(10)
                        self.game_map.player.increase_max_stamina(20)
                        self.game_map.player.increase_strength(1)
                        if self.game_map.player.get_level() == 5:
                            self.game_map.map_image = pygame.image.load(GAME_ASSETS["dungeon_map1"]).convert_alpha()
                            self.game_map.map_image = pygame.transform.scale(self.game_map.map_image, (self.game_map.window.get_width(), self.game_map.window.get_height()))
                            self.game_map.reload_mobs()  # Reload the mobs
                        if self.game_map.player.get_level() == 9 and not self.game_map.boss_spawned:
                            self.game_map.spawn_boss()
                            self.game_map.boss_spawned = True
                        self.game_map.in_combat = False
                        self.state = 'game_map'

                    elif result == 'player_attacked':
                        continue
                    elif result == 'run_successful':
                        print("You successfully ran away!")
                        self.game_map.last_run_time = time.time()  # Set the last run time
                        self.game_map.in_combat = False
                        self.state = 'game_map'
                    elif result == 'run_failed':
                        continue
                else:
                    result = self.turnbased.enemy_attack()
                    if result == 'player_defeated':
                        print("You were defeated!")
                        self.state = 'game_over'
                    elif result == 'enemy_attacked':
                        continue

            elif self.state == 'game_over':
                self.turnbased.display_dead_screen()

if __name__ == "__main__":
    game = Game()
    game.run()