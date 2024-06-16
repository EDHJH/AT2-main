from character import Character

class Necromancer(Character):
    def __init__(self, name):
        super().__init__(name, "Necromancer", armour = 5)
        # Additional attributes and methods specific to the Mage class
