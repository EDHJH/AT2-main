from character import Character

class Ranger(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Ranger", armour = 7)
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regeneration = 10
        self.strength = 10
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attacks = {
            "Arrow Shot": {"method": self.arrow_shot, "stamina_cost": 10},
            "Charged Arrow": {"method": self.charge, "stamina_cost": 20},
            "Lightning Arrow": {"method": self.charge, "stamina_cost": 25},
            
        }



class Warrior(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Warrior", armor=10)
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regeneration = 10
        self.strength = 15
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attacks = {
            "Basic Attack": {"method": self.basic_attack, "stamina_cost": 10},
            "Charge": {"method": self.charge, "stamina_cost": 20},
            "Cleave Attack": {"method": self.cleave_attack, "stamina_cost": 30},
            "Shield Bash": {"method": self.shield_bash, "stamina_cost": 15},
            "Defensive Stance": {"method": self.defensive_stance, "stamina_cost": 5},
        }
