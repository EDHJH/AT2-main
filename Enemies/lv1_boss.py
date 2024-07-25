import pygame, random
from Enemies.enemy import Enemy

class Lv1Boss(Enemy):
    def __init__(self, position, window):
        super().__init__('AT2/assets/lv1_boss.png', position, window, name="Lv1Boss")
        self.max_health = 300  # Boss has more health
        self.health = self.max_health
        self.attack_damage = 20  # Boss deals more damage

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has been defeated!")
            return True
        return False

    def attack(self, target):
        damage = random.randint(self.attack_damage - 5, self.attack_damage + 5)  # Boss has a higher damage range
        print(f"\n{self.name} attacks {target.get_name()} and deals {damage} damage!")
        target.take_damage(damage)
        return damage

