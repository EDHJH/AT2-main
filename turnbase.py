class Turnbased:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player_turn = True

    def player_attack(self):
        if self.player_turn:
            damage = self.player.choose_attack(self.enemy)
            print(f"Player attacks! Deals {damage} damage to the enemy.")
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
