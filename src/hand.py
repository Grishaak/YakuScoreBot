import random

from src.wall import Wall


class Hand:

    def __init__(self, wall: Wall):
        self.wall_data = wall
        self.your_hand = list()
        self.data_hand = self.hand_creator()

    def __pon_creator(self):
        """Create a set"""
        data_set = 'pon'
        fu_pon = 4
        status_set = 'closed'
        is_open = True if random.randint(1, 9) == 1 else False
        while True:
            suit = self.wall_data.choose_random_suit(data_set)
            number = self.wall_data.choose_random_number(suit, data_set)
            set_tiles = list(self.wall_data.ALL_TILES[suit].items())[number]
            tile = set_tiles[0]
            if self.wall_data.ALL_TILES[suit][tile] >= 3:
                self.wall_data.ALL_TILES[suit][tile] -= 3
                for key, values in self.wall_data.TILE_DATA['pon'].items():
                    if set_tiles[0] in values:
                        new_key = key + '_pons'
                        self.data_hand[new_key] += 1
                        fu_pon += 4
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                pon = set_tiles[0] * 3
                if is_open:
                    fu_pon //= 2
                    pon = set_tiles[0] + '-' + set_tiles[0] * 2
                    self.data_hand['opened_pons'] += 1
                    self.data_hand['is_open'] = True
                    status_set = 'opened'
                self.data_hand['additional_fu'] += fu_pon
                return pon, 'pon', str(number) * 3 + suit, status_set

    def __kan_creator(self):
        """Create a kan"""
        data_set = 'pon'
        fu_kan = 16
        is_open = False if random.randint(1, 4) == 1 else True
        status_set = 'closed'
        while True:
            suit = self.wall_data.choose_random_suit(data_set)
            number = self.wall_data.choose_random_number(suit, data_set)
            set_tiles = list(self.wall_data.ALL_TILES[suit].items())[number]
            tile = set_tiles[0]
            if self.wall_data.ALL_TILES[suit][tile] > 3:
                self.wall_data.ALL_TILES[suit][tile] -= 4
                for key, values in self.wall_data.TILE_DATA['kan'].items():
                    if set_tiles[0] in values:
                        new_key = key + '_kans'
                        self.data_hand[new_key] += 1
                        fu_kan += 16
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                if is_open:
                    fu_kan = fu_kan // 2
                    kan = set_tiles[0] + '-' + set_tiles[0] * 3
                    self.data_hand['opened_kans'] += 1
                    self.data_hand['is_open'] = True
                    status_set = 'opened'
                else:
                    kan = self.wall_data.SPECIAL_TILE + set_tiles[0] * 2 + self.wall_data.SPECIAL_TILE
                self.data_hand['additional_fu'] += fu_kan
                return kan, 'kan', str(number) * 4 + suit, status_set

    def __chi_creator(self):
        """Create a chi"""
        while True:
            data_set = 'chi'
            chi = ''
            status_set = 'closed'
            i = 0
            suit = self.wall_data.choose_random_suit(data_set)
            number = self.wall_data.choose_random_number(suit, data_set)
            set_tiles = list(self.wall_data.ALL_TILES[suit].items())[number: number + 3]
            flag = False
            while i < 3:
                if set_tiles[i][1] < 1:
                    chi = ''
                    break
                else:
                    chi += set_tiles[i][0]
                    i += 1
            if len(chi) > 2:
                flag = True
            if flag:
                for i in chi:
                    if i in self.wall_data.TILE_DATA['chi']['border']:
                        self.data_hand['border_chis'] += 1
                        break
                is_open = True if random.randint(1, 6) == 1 else False
                if is_open:
                    chi = list(chi)
                    x = chi.pop(random.randrange(3))
                    chi = x + '-' + "".join(chi)
                    self.data_hand['opened_chis'] += 1
                    self.data_hand['is_open'] = True
                    status_set = 'opened'
                self.data_hand[suit + '_sets'] += 1
                numbers = "".join([str(i) for i in range(number, number + 3)])
                return chi, 'chi', numbers + suit, status_set

    def __pair_creator(self):
        """Create a pair"""
        status_set = 'closed'
        data_set = 'pon'
        while True:
            suit = self.wall_data.choose_random_suit(data_set)
            number = self.wall_data.choose_random_number(suit, data_set)
            set_tiles = list(self.wall_data.ALL_TILES[suit].items())[number]
            tile = set_tiles[0]
            if (self.wall_data.ALL_TILES[suit][tile] >= 2) and (self.data_hand['is_chiitoi'] != True):
                self.wall_data.ALL_TILES[suit][tile] -= 2
                for key, values in self.wall_data.TILE_DATA['pair'].items():
                    if set_tiles[0] in values:
                        if (set_tiles[0] == self.data_hand['prevailed_wind'] or set_tiles[0] == self.data_hand[
                            'your_wind']
                                or suit == 'dragon'):
                            self.data_hand['additional_fu'] += 2
                        new_key = key + '_pair'
                        self.data_hand[new_key] += 1
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                return set_tiles[0] * 2, 'pair', str(number) * 2 + suit, status_set
            elif (self.data_hand['is_chiitoi'] == True) and (self.wall_data.ALL_TILES[suit][tile] > 3):
                self.wall_data.ALL_TILES[suit][tile] -= 2
                for key, values in self.wall_data.TILE_DATA['pair'].items():
                    if set_tiles[0] in values:
                        if (set_tiles[0] == self.data_hand['prevailed_wind'] or set_tiles[0] == self.data_hand[
                            'your_wind']
                                or suit == 'dragon'):
                            self.data_hand['additional_fu'] += 2
                        new_key = key + '_pair'
                        self.data_hand[new_key] += 1
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                return set_tiles[0] * 2, 'pair', str(number) * 2 + suit, status_set

    def __chiitoi_create(self):
        self.data_hand["is_chiitoi"] = True
        count = 0
        while count != 7:
            pair = self.__pair_creator()
            while pair in self.your_hand:
                pair = self.__pair_creator()
            else:
                self.your_hand.append(pair)
                count += 1

    def hand_creator(self):
        """Here is collected all chi pon or pairs sets to create a ready hand"""
        pon_chance = True if (random.randint(0, 100) <= 17) else False
        kan_chance = True if (random.randint(0, 100) <= 15) else False
        is_chiitoi = True if random.choice(range(20)) == 1 else False
        self.data_hand = {"yaku": dict(), "is_valid": True, "base_fu": 0, "additional_fu": 0, "base_han": 0,
                          "dora_pointers": '', "dora": '', "dora_amount": 0, 'is_open': False, 'tsumo': False,
                          'ron': False,
                          'manzu_sets': 0, 'souzu_sets': 0, 'pinzu_sets': 0, 'honor_sets': 0, "chi_amount": 0,
                          "pon_amount": 0, "kan_amount": 0, 'opened_pons': 0, 'opened_kans': 0, 'opened_chis': 0,
                          'two_identical_chi_in_same_suit': 0, 'identical_chi_in_diff_suits': 0, 'identical_pons': 0,
                          'in_one_suit': False, 'full_suit': False, 'border_pons': 0, 'border_kans': 0,
                          'border_chis': 0,
                          'border_pair': 0, 'wind_pons': 0, 'wind_kans': 0, 'wind_pair': 0, 'dragon_pons': 0,
                          'dragon_kans': 0, 'dragon_pair': 0,
                          'prevailed_wind': random.choice(self.wall_data.TILES_DICT["wind"][:2]),
                          'your_wind': random.choice(self.wall_data.TILES_DICT["wind"][::]), "is_chiitoi": False}
        if is_chiitoi:
            self.__chiitoi_create()
            self.data_hand["base_fu"] = 25
            self.data_hand["base_han"] += 2
            self.data_hand["hand"] = self.your_hand
            self.data_hand["yaku"]["chiitoi"] = True
        else:
            for _ in range(4):
                if pon_chance:
                    if kan_chance:
                        kan = self.__kan_creator()
                        self.your_hand.append(kan)
                        self.data_hand["kan_amount"] += 1
                    else:
                        pon = self.__pon_creator()
                        self.your_hand.append(pon)
                        self.data_hand["pon_amount"] += 1
                else:
                    hand_created = self.__chi_creator()
                    self.your_hand.append(hand_created)
                    self.data_hand["chi_amount"] += 1
            self.your_hand.append(self.__pair_creator())
            self.data_hand["hand"] = self.your_hand
        return self.data_hand

    def __count_doras(self, doras: dict):
        pass

    def yaku_calculator(self):

        riichi_chance = True if random.randint(0, 100) <= 35 else False
        ippatsu_chance = True if random.randint(0, 100) <= 17 else False
        tsumo_chance = True if random.randint(0, 100) >= 50 else False
        hoitei_haitei_chance = True if random.randint(0, 100) <= 5 else False
        pointer_dora = self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
        pointer_ura_dora = self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
        pointer_kan_dora = [self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
                            for i in range(self.data_hand['kan_amount'])]
        pointer_kan_ura_dora = [self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
                                for i in range(self.data_hand['kan_amount'])]
        doras = self.wall_data.find_all_doras(pointer_dora, pointer_ura_dora, pointer_kan_dora,
                                              pointer_kan_ura_dora)
        self.data_hand['dora_pointers'] = {'dora_pointers': [pointer_dora, *pointer_kan_dora],
                                           'ura_dora_pointers': [pointer_ura_dora, *pointer_kan_ura_dora]}
        if riichi_chance:
            self.data_hand['yaku']['riichi'] = True
            self.data_hand['base_han'] += 1
            if ippatsu_chance:
                self.data_hand['yaku']['ippatsu'] = True
                self.data_hand['base_han'] += 1

        if tsumo_chance:
            if not self.data_hand['is_open']:
                self.data_hand['yaku']['menzen_tsumo'] = True
                self.data_hand['base_han'] += 1
            self.data_hand['base_fu'] = 20
            self.data_hand['tsumo'] = True
            self.data_hand['additional_fu'] += 2
        else:
            self.data_hand['base_fu'] = 20
            if not self.data_hand['is_open']:
                self.data_hand['yaku']['menzen_tsumo'] = True
                self.data_hand['base_fu'] += 10
            self.data_hand['ron'] = True

        # Checking the chance for last draw winning tile or ron on last discard.
        if hoitei_haitei_chance:
            self.data_hand['yaku']['hotei'] = True
            self.data_hand['base_han'] += 1

        if not self.data_hand['additional_fu']:
            self.data_hand['additional_fu'] += 2

        for set_tile in self.data_hand['hand']:
            for tile in set_tile[0]:
                for dora in doras['doras']:
                    if tile == dora:
                        self.data_hand['dora_amount'] += 1
                if self.data_hand['yaku'].get('riichi'):
                    for dora in doras['doras']:
                        if tile == dora:
                            self.data_hand['dora_amount'] += 1
        self.data_hand['dora'] = doras
        self.data_hand['pretty_dead_wall'] = self.build_dead_wall()
        self.data_hand['pretty_hand'] = self.build_hand()

    def build_dead_wall(self):
        number_right = 2 - (self.data_hand['kan_amount'] // 2)
        number_left = 4 - (self.data_hand['kan_amount'] // 2)
        wall = (self.wall_data.SPECIAL_TILE * number_left) + "".join(i for i in self.data_hand['dora']['doras']) + (
                self.wall_data.SPECIAL_TILE * number_right)
        return wall

    def build_hand(self):
        x = sorted([i[0] for i in sorted(self.data_hand['hand'], key=lambda x: x[3], reverse=True)])
        print(x)
        return "".join(x)

    def get_data_hand(self):
        return self.data_hand

    def get_your_hand(self):
        return self.your_hand
