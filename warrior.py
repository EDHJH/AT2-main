from character import Character

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

    def choose_attack(self, target):
        print(f"Choose an attack (Current stamina: {self.__current_stamina}):")
        attack_list = list(self.__attacks.items())
        for i, (attack, info) in enumerate(attack_list):
            print(f"{i + 1}. {attack} (Stamina cost: {info['stamina_cost']})")
        chosen_attack = int(input("Enter the number of the attack: "))
        if 1 <= chosen_attack <= len(attack_list):
            attack, attack_info = attack_list[chosen_attack - 1]
            if self.__current_stamina >= attack_info["stamina_cost"]:
                self.__current_stamina -= attack_info["stamina_cost"]
                attack_method = attack_info["method"]
                attack_method(target)
            else:
                print("Not enough stamina for this attack.")
        else:
            print("Invalid attack.")

    def regenerate_stamina(self):
        self.__current_stamina = min(self.__max_stamina, self.__current_stamina + self.__stamina_regeneration)

    def attack(self, target):
        damage = self.__strength * self.get_level()
        target.take_damage(damage)
        return damage

    def charge(self, target):
        print(f"{self.get_name()} charges towards {target.get_name()}!")
        target.take_damage(self.__strength)

    def basic_attack(self, target):
        damage = self.__strength
        print(f"{self.get_name()} performs a basic attack on {target.get_name()} for {damage} damage!")
        target.take_damage(damage)

    def cleave_attack(self, targets):
        total_damage = 0
        for target in targets:
            damage = self.__strength * 2
            total_damage += damage
            print(f"{self.get_name()} cleaves {target.get_name()} for {damage} damage!")
            target.take_damage(damage)
        print(f"{self.get_name()} dealt a total of {total_damage} damage with cleave!")

    def shield_bash(self, target):
        damage = self.__strength + 5
        print(f"{self.get_name()} performs a shield bash on {target.get_name()} for {damage} damage!")
        target.take_damage(damage)

    def defensive_stance(self):
        self.set_armor_class(self.get_armor_class() + 5)
        print(f"{self.get_name()} enters a defensive stance, increasing armor class!")

    # Getter methods
    def get_max_stamina(self):
        return self.__max_stamina

    def get_current_stamina(self):
        return self.__current_stamina

    def get_stamina_regeneration(self):
        return self.__stamina_regeneration

    def get_strength(self):
        return self.__strength

    def get_max_hp(self):
        return self.__max_hp

    def get_current_hp(self):
        return self.__current_hp

    def get_attacks(self):
        return self.__attacks

    # Setter methods
    def set_max_stamina(self, max_stamina):
        self.__max_stamina = max_stamina

    def set_current_stamina(self, current_stamina):
        self.__current_stamina = current_stamina

    def set_stamina_regeneration(self, stamina_regeneration):
        self.__stamina_regeneration = stamina_regeneration

    def set_strength(self, strength):
        self.__strength = strength

    def set_max_hp(self, max_hp):
        self.__max_hp = max_hp

    def set_current_hp(self, current_hp):
        self.__current_hp = current_hp

    def set_attacks(self, attacks):
        self.__attacks = attacks

