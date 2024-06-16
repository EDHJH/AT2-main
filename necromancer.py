from character import Character

class Necromancer(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Necromancer", armour = 7)
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regeneration = 10
        self.strength = 10
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attacks = {
            "Arrow Shot": {"method": self.arrow_shot, "stamina_cost": 10},
            "Charged Arrow": {"method": self.charged_arrow, "stamina_cost": 20},
            "Lightning Arrow": {"method": self.lightning_arrow, "stamina_cost": 25},
            "Rain of Arrows": {"method": self.rain_of_arrows, "stamina_cost": 50}
        }