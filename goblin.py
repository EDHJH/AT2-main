# goblin.py
import random
from enemy import Enemy

class Goblin(Enemy):
    def move(self):
        self.set_position([
            self.get_position()[0] + random.randint(-10, 10),
            self.get_position()[1] + random.randint(-10, 10)
        ])
        self.set_position([
            max(0, min(self.get_window().get_width() - self.get_image().get_width(), self.get_position()[0])),
            max(0, min(self.get_window().get_height() - self.get_image().get_height(), self.get_position()[1]))
        ])