from Characters.character import Character

#Setting Attributes


class Warrior(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Warrior", armor=10)
        self.__max_stamina = 100
        self.__current_stamina = self.__max_stamina
        self.__stamina_regeneration = 10
        self.__strength = 15
        self.__max_hp = max_hp
        self.__current_hp = max_hp
        self.__attacks = {
            "Basic Attack": {"method": self.basic_attack, "stamina_cost": 10},
            "Charge": {"method": self.charge, "stamina_cost": 20},
            "Cleave Attack": {"method": self.cleave_attack, "stamina_cost": 30},
            "Shield Bash": {"method": self.shield_bash, "stamina_cost": 15},
            "Defensive Stance": {"method": self.defensive_stance, "stamina_cost": 5},
        }

    # Getter Methods
    def getMax_stamina(self):
        return self.__max_stamina
    
    def getCurrent_stamina(self):
        return self.__current_stamina

    def getStamina_regeneration(self):
        return self.__stamina_regeneration
    
    def getStrength(self):
        return self.__strength
    
    def getAttacks(self):
        return self.__attacks

    def getMaxhp(self):
        return self.__max_hp
    
    def getCurrent_hp(self):
        return self.__current_hp

    # Functions
    def regenerate_stamina(self):
        self.current_stamina = min(self.getMax_stamina, self.current_stamina + self.getStamina_regeneration)

    def attack(self, target):
        # Calculate damage based on warrior's level, strength, and any weapon modifiers
        # For simplicity, let's assume the warrior's damage is directly proportional to their level
        damage = self.getStrength*self.getLevel
        target.take_damage(damage)  # Apply damage to the target
        return damage  # Return the amount of damage dealt

    def charge(self, target):
        print(f"{self.getName} charges towards {target.name}!")
        target.take_damage(self.getStrength)  # Example: Charge deals damage equal to the warrior's strength

    def basic_attack(self, target):
        damage = self.strength  # Example: Basic attack damage equals warrior's strength
        print(f"{self.getName} performs a basic attack on {target} for {damage} damage!")
        target.take_damage(damage)

    def cleave_attack(self, targets):
        total_damage = 0
        for target in targets:
            damage = self.getStrength * 2  # Example: Cleave attack deals double the warrior's strength to each target
            total_damage += damage
            print(f"{self.getName} cleaves {target} for {damage} damage!")
            target.take_damage(damage)
        print(f"{self.getName} dealt a total of {total_damage} damage with cleave!")

    def shield_bash(self, target):
        damage = self.strength + 5  # Example: Shield bash deals warrior's strength plus 5 additional damage
        print(f"{self.getName} performs a shield bash on {target} for {damage} damage!")
        target.take_damage(damage)

    def defensive_stance(self):
        self.getArmor_class += 5  # Example: Defensive stance increases armor class by 5
        print(f"{self.getName} enters a defensive stance, increasing armor class!")
