class Warrior:
    def __init__(self):
        self.health = 50
        self.attack = 5
        self.defense = 0
        self.vampirism = 0
        self.splash = 0

    @property
    def is_alive(self) -> bool:
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.attack = 7


class Defender(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.attack = 3
        self.defense = 2


class Vampire(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 40
        self.attack = 4
        self.vampirism = 50


class Lancer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.attack = 6
        self.splash = .5


####################################################################

class Army:
    def __init__(self):
        self.soldiers = []

    def add_units(self, unit, quantity):
        print("Adding:", unit.__name__, quantity)
        self.soldiers += [unit() for i in range(quantity)]
        print(len(self.soldiers), "total")


class Battle:
    def fight(self, army_1, army_2):
        print("Battle:", len(army_1.soldiers), "vs", len(army_2.soldiers))
        for i in range(1000):
            print("Scene", i)
            print(''.join(['+' * s.is_alive + '_' * (not s.is_alive) for s in army_1.soldiers]))
            print(''.join(['+' * s.is_alive + '_' * (not s.is_alive) for s in army_2.soldiers]))

            alive_1 = [s for s in army_1.soldiers if s.is_alive]
            alive_2 = [s for s in army_2.soldiers if s.is_alive]

            alive_count_1, alive_count_2 = len(alive_1), len(alive_2)

            if alive_count_2 == 0:
                print("Army 1 won!\n")
                return True
            elif alive_count_1 == 0:
                print("Army 2 won!\n")
                return False
            else:
                current_1 = alive_1[0]
                current_2 = alive_2[0]
                if alive_count_1 > 1:
                    back_1 = alive_1[1]
                    print("Back 1 is", back_1)
                else:
                    back_1 = None
                if alive_count_2 > 1:
                    back_2 = alive_2[1]
                    print("Back 2 is", back_2)
                else:
                    back_2 = None

                fight(current_1, current_2, back_1=back_1, back_2=back_2)


def fight(unit_1, unit_2, **kwargs):
    print(f"{unit_1.__class__.__name__}[{unit_1.health} {unit_1.attack} {unit_1.defense}] vs " +
          f"{unit_2.__class__.__name__}[{unit_2.health} {unit_2.attack} {unit_2.defense}]")
    for i in range(100):
        ### 1 hits 2
        damage_1_to_2 = max(unit_1.attack - unit_2.defense, 0)
        unit_2.health -= damage_1_to_2
        print(f"Round {i}: {unit_1.health:2.0f} > {unit_2.health:2.0f}")

        # splash 1
        back_2 = kwargs.get('back_2', None)
        if unit_1.splash > 0 and back_2:
            splash_1_to_back_2 = unit_1.splash * max((unit_1.attack - back_2.defense), 0)
            print("slash to back 2:", splash_1_to_back_2)
            back_2.health -= splash_1_to_back_2

        # vampirism 1
        vampirism_1 = round(damage_1_to_2 * unit_1.vampirism / 100)
        if vampirism_1 > 0:
            unit_1.health += vampirism_1
            print("vampirism by 1:", vampirism_1)

        ### 2 hits 1
        if unit_2.health > 0:
            damage_2_to_1 = max(unit_2.attack - unit_1.defense, 0)
            unit_1.health -= damage_2_to_1
            print(f"{unit_1.health:{11 + i // 10}.0f} < {unit_2.health:2.0f}")

            # splash 2
            back_1 = kwargs.get('back_1', None)
            if unit_2.splash > 0 and back_1:
                splash_2_to_back_1 = unit_2.splash * max((unit_2.attack - back_1.defense), 0)
                print(f"slash to back 1: {splash_2_to_back_1:2}")
                back_1.health -= splash_2_to_back_1

            # vampirism 2
            vampirism_2 = round(damage_2_to_1 * unit_2.vampirism / 100)
            if vampirism_2 > 0:
                unit_2.health += vampirism_2
                print("vampirism by 2:", vampirism_2)

        # alive check
        if unit_2.health <= 0:
            print("Unit 1 won!\n")
            return True
        if unit_1.health <= 0:
            print("Unit 2 won!\n")
            return False
    return Error


if __name__ == '__main__':

    # # fight tests
    # chuck = Warrior()
    # bruce = Warrior()
    # carl = Knight()
    # dave = Warrior()
    # mark = Warrior()
    # bob = Defender()
    # mike = Knight()
    # rog = Warrior()
    # lancelot = Defender()
    # eric = Vampire()
    # adam = Vampire()
    # richard = Defender()
    # ogre = Warrior()
    # freelancer = Lancer()
    # vampire = Vampire()
    #
    # assert fight(chuck, bruce) == True
    # assert fight(dave, carl) == False
    # assert chuck.is_alive == True
    # assert bruce.is_alive == False
    # assert carl.is_alive == True
    # assert dave.is_alive == False
    # assert fight(carl, mark) == False
    # assert carl.is_alive == False
    # assert fight(bob, mike) == False
    # assert fight(lancelot, rog) == True
    # assert fight(eric, richard) == False
    # assert fight(ogre, adam) == True
    # assert fight(freelancer, vampire) == True
    # assert freelancer.is_alive == True
    #
    # # battle tests
    # my_army = Army()
    # my_army.add_units(Defender, 2)
    # my_army.add_units(Vampire, 2)
    # my_army.add_units(Lancer, 4)
    # my_army.add_units(Warrior, 1)
    #
    # enemy_army = Army()
    # enemy_army.add_units(Warrior, 2)
    # enemy_army.add_units(Lancer, 2)
    # enemy_army.add_units(Defender, 2)
    # enemy_army.add_units(Vampire, 3)
    #
    # army_3 = Army()
    # army_3.add_units(Warrior, 1)
    # army_3.add_units(Lancer, 1)
    # army_3.add_units(Defender, 2)
    #
    # army_4 = Army()
    # army_4.add_units(Vampire, 3)
    # army_4.add_units(Warrior, 1)
    # army_4.add_units(Lancer, 2)
    #
    # battle = Battle()
    #
    # assert battle.fight(my_army, enemy_army) == True
    # assert battle.fight(army_3, army_4) == False

    # # mission check tests
    #
    # army_1 = Army()
    # army_2 = Army()
    # army_1.add_units(Defender, 11)
    # army_1.add_units(Vampire, 3)
    # army_1.add_units(Warrior, 4)
    # army_2.add_units(Warrior, 4)
    # army_2.add_units(Defender, 4)
    # army_2.add_units(Vampire, 13)
    # battle = Battle()
    # 
    # assert battle.fight(army_1, army_2) == True





    # mission check tests

    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Defender, 11)
    army_1.add_units(Vampire, 3)
    army_1.add_units(Warrior, 4)
    army_2.add_units(Warrior, 4)
    army_2.add_units(Defender, 4)
    army_2.add_units(Vampire, 13)
    battle = Battle()

    assert battle.fight(army_1, army_2) == True