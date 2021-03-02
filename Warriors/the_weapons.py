from contextlib import suppress


class Warrior:
    warriors_count = 0
    _max_health = 50
    _attack = 5
    _defense = 0
    _vampirism = 0
    _splash = 0
    _heal_power = 0

    def __init__(self, *args, **kwargs):
        self._health = type(self)._max_health
        self.equipment = []
        self.warrior_id = Warrior.warriors_count
        Warrior.warriors_count += 1

    def __repr__(self):
        repr_string = ''
        repr_string += f'{self.__class__.__name__} ({self.warrior_id}) '
        repr_string += f'HP: {self.health}/{self.max_health}({type(self)._max_health})\n'
        for element in self.equipment:
            repr_string += f'{element}\n'
        repr_string += f'Basic:    A:{type(self)._attack} D:{type(self)._defense} '
        repr_string += f'V:{type(self)._vampirism} S:{type(self)._splash} H:{type(self)._heal_power}\n'
        repr_string += f'Modified: A:{self.attack} D:{self.defense} '
        repr_string += f'V:{self.vampirism} S:{self.splash} H:{self.heal_power}'
        return repr_string

    @property
    def health(self):
        return self._health

    @property
    def max_health(self):
        return self.get_parameter('_max_health')

    @property
    def attack(self):
        return self.get_parameter('_attack')

    @property
    def defense(self):
        return self.get_parameter('_defense')

    @property
    def vampirism(self):
        return self.get_parameter('_vampirism')

    @property
    def splash(self):
        return self._splash

    @property
    def heal_power(self):
        return self.get_parameter('_heal_power')

    @property
    def is_alive(self):
        return self.health > 0

    def get_parameter(self, parameter):
        if getattr(type(self), parameter) == 0:
            return 0
        parameter_by_equipment = sum(getattr(e, parameter[1:]) for e in self.equipment)
        return getattr(type(self), parameter) + parameter_by_equipment

    def add_health(self, health_delta):
        self._health += health_delta

    def hit(self, defender, hit_mode):
        damage_dealt = defender.receive_hit(self, hit_mode)
        self.vampirate(damage_dealt)

    def receive_hit(self, attacker, hit_mode):
        if hit_mode == 'attack':
            damage = attacker.attack
        elif hit_mode == 'splash':
            damage = attacker.attack * attacker.splash
        else:
            raise ValueError

        damage_limited = max(damage - self.defense, 0)
        damage_received = min(damage_limited, self.health)

        self.add_health(-damage_received)
        return damage_received

    def vampirate(self, damage_dealt):
        vampirism_hp_received = int(damage_dealt * self.vampirism / 100)
        hp_to_maximum = self.max_health - self.health

        vampirism_hp_used = min(vampirism_hp_received, hp_to_maximum)
        self.add_health(vampirism_hp_used)

    def heal(self, heal_target):
        if not heal_target.is_alive or not self.is_alive:
            return
        hp_to_maximum = heal_target.max_health - heal_target.health
        healed_hp = min(self.heal_power, hp_to_maximum)
        heal_target.add_health(healed_hp)

    def equip_weapon(self, weapon_name):
        print('Equipping:')
        self.equipment.append(weapon_name)
        self.add_health(weapon_name.health)
        print(self)
        print()


class Knight(Warrior):
    _attack = 7


class Defender(Warrior):
    _max_health = 60
    _attack = 3
    _defense = 2


class Vampire(Warrior):
    _max_health = 40
    _attack = 4
    _vampirism = 50


class Lancer(Warrior):
    _attack = 6
    _splash = 0.5


class Healer(Warrior):
    _max_health = 60
    _attack = 0
    _heal_power = 2


# class Rookie(Warrior):
#     _max_health = 50
#     _attack = 1

class Rookie(Warrior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health = 50
        self.attack = 1


class Weapon:
    weapons_count = 0
    _health = 0
    _attack = 0
    _defense = 0
    _vampirism = 0
    _heal_power = 0

    def __init__(self, *args):
        if args:
            self.health = args[0]
            self.max_health = args[0]
            self.attack = args[1]
            self.defense = args[2]
            self.vampirism = args[3]
            self.heal_power = args[4]
        else:
            self.health = type(self)._health
            self.max_health = type(self)._health
            self.attack = type(self)._attack
            self.defense = type(self)._defense
            self.vampirism = type(self)._vampirism
            self.heal_power = type(self)._heal_power
        self.weapon_id = Weapon.weapons_count
        Weapon.weapons_count += 1

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.weapon_id}) {self.__dict__}'


class Sword(Weapon):
    _health = 5
    _attack = 2


class Shield(Weapon):
    _health = 20
    _attack = -1
    _defense = 2


class GreatAxe(Weapon):
    _health = -15
    _attack = 5
    _defense = -2
    _vampirism = 10


class Katana(Weapon):
    _health = -20
    _attack = 6
    _defense = -5
    _vampirism = 50


class MagicWand(Weapon):
    _health = 30
    _attack = 3
    _heal_power = 3


class Army:
    armies_count = 0

    def __init__(self, units=None):
        if units is None:
            units = []
        self.units = units.copy()
        self.army_id = Army.armies_count
        Army.armies_count += 1

    def __repr__(self):
        return f'{self.__class__.__name__} {self.army_id}'

    def add_units(self, unit, unit_count):
        for _ in range(unit_count):
            # self.units.insert(0, unit())
            self.units.append(unit())

    def attack(self, defending_army):
        return defending_army.receive_attack(self)

    def receive_attack(self, attacking_army):
        first_defending_unit = self.units[-1]
        first_attacking_unit = attacking_army.units[-1]
        first_attacking_unit.hit(first_defending_unit, hit_mode='attack')

        with suppress(IndexError):
            second_defending_unit = self.units[-2]
            first_attacking_unit.hit(second_defending_unit, hit_mode='splash')
            second_defending_unit.heal(first_defending_unit)

            if not second_defending_unit.is_alive:
                self.units.remove(second_defending_unit)

        if not first_defending_unit.is_alive:
            self.units.remove(first_defending_unit)
            return True


class Battle:
    @staticmethod
    def fight(army_a, army_b):

        while True:
            for attacking_army, defending_army in (army_a, army_b), (army_b, army_a):

                is_defender_perished = attacking_army.attack(defending_army)

                if not defending_army.units:
                    # print('Winner:', attacking_army)
                    return defending_army == army_b

                if is_defender_perished:
                    break

    @staticmethod
    def straight_fight(army_a, army_b):

        while True:
            for unit_a, unit_b in zip(reversed(army_a.units.copy()),
                                      reversed(army_b.units.copy())):

                is_defender_perished = fight(unit_a, unit_b)

                if is_defender_perished:
                    army_b.units.remove(unit_b)
                else:
                    army_a.units.remove(unit_a)

            if not army_b.units:
                # print('Army A won')
                return True

            if not army_a.units:
                # print('Army B won')
                return False


def fight(unit_a, unit_b):
    return Battle.fight(Army([unit_a]), Army([unit_b]))


if __name__ == '__main__':
    # ogre = Warrior()
    # lancelot = Knight()
    # richard = Defender()
    # eric = Vampire()
    # freelancer = Lancer()
    # priest = Healer()
    #
    # sword = Sword()
    # shield = Shield()
    # axe = GreatAxe()
    # katana = Katana()
    # wand = MagicWand()
    # super_weapon = Weapon(50, 10, 5, 150, 8)
    #
    # ogre.equip_weapon(sword)
    # ogre.equip_weapon(shield)
    # ogre.equip_weapon(super_weapon)
    # lancelot.equip_weapon(super_weapon)
    # richard.equip_weapon(shield)
    # eric.equip_weapon(super_weapon)
    # freelancer.equip_weapon(axe)
    # freelancer.equip_weapon(katana)
    # priest.equip_weapon(wand)
    # priest.equip_weapon(shield)
    #
    # assert ogre.health == 125
    # assert lancelot.attack == 17
    # assert richard.defense == 4
    # assert eric.vampirism == 200
    # assert freelancer.health == 15
    # assert priest.heal_power == 5
    #
    # assert fight(ogre, eric) == False
    # assert fight(priest, richard) == False
    # assert fight(lancelot, freelancer) == True
    #
    # my_army = Army()
    # my_army.add_units(Knight, 1)
    # my_army.add_units(Lancer, 1)
    #
    # enemy_army = Army()
    # enemy_army.add_units(Vampire, 1)
    # enemy_army.add_units(Healer, 1)
    #
    # my_army.units[0].equip_weapon(axe)
    # my_army.units[1].equip_weapon(super_weapon)
    #
    # enemy_army.units[0].equip_weapon(katana)
    # enemy_army.units[1].equip_weapon(wand)
    #
    # battle = Battle()
    #
    # assert battle.fight(my_army, enemy_army) == True

    # mission tests

    weapon_1 = Katana()
    weapon_2 = Shield()

    my_army = Army()
    my_army.add_units(Vampire, 2)
    my_army.add_units(Rookie, 2)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 1)
    enemy_army.add_units(Defender, 2)

    my_army.units[0].equip_weapon(weapon_1)
    my_army.units[1].equip_weapon(weapon_1)
    my_army.units[2].equip_weapon(weapon_2)

    enemy_army.units[0].equip_weapon(weapon_1)
    enemy_army.units[1].equip_weapon(weapon_2)
    enemy_army.units[2].equip_weapon(weapon_2)

    battle = Battle()

    assert battle.straight_fight(my_army, enemy_army) == True