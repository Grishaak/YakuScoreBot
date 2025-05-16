import random

from src.wall import Wall
from src.yaku_list import *


class Hand:

    def __init__(self, wall: Wall):
        self.wall_data = wall
        self.your_hand = list()
        self.data_hand = self.hand_creator()

    def __pon_creator(self, is_chonroto=False):
        """Create a set"""
        data_set = 'pon'
        status_set = 'closed'
        is_open = False if random.randint(1, 4) == 1 else True
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
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                pon = set_tiles[0] * 3
                if is_open:
                    pon = set_tiles[0] + '-' + set_tiles[0] * 2
                    self.data_hand['opened_pons'] += 1
                    self.data_hand['is_open'] = True
                    status_set = 'opened'
                return [pon, 'pon', str(number) * 3 + suit, status_set]

    def __kan_creator(self):
        """Create a kan"""
        data_set = 'pon'
        is_open = False if random.randint(1, 3) == 2 else True
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
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                if is_open:
                    kan = set_tiles[0] + '-' + set_tiles[0] * 3
                    self.data_hand['opened_kans'] += 1
                    self.data_hand['is_open'] = True
                    status_set = 'opened'
                else:
                    kan = self.wall_data.SPECIAL_TILE + set_tiles[0] * 2 + self.wall_data.SPECIAL_TILE
                return [kan, 'kan', str(number) * 4 + suit, status_set]

    def __chi_creator(self, is_chonroto=False):
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
                for j in chi:
                    self.wall_data.ALL_TILES[suit][j] -= 1
                if is_open:
                    chi = list(chi)
                    x = chi.pop(random.randrange(3))
                    chi = x + '-' + "".join(chi)
                    self.data_hand['opened_chis'] += 1
                    self.data_hand['is_open'] = True
                    status_set = 'opened'
                self.data_hand[suit + '_sets'] += 1
                numbers = "".join([str(i) for i in range(number, number + 3)])

                return [chi, 'chi', numbers + suit, status_set]

    def __pair_creator(self, is_chonroto=False):
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
                        # if (set_tiles[0] == self.data_hand['prevailed_wind'] or set_tiles[0] == self.data_hand[
                        #     'your_wind']
                        #         or suit == 'dragon'):
                        #     self.data_hand['additional_fu'] += 2
                        new_key = key + '_pair'
                        self.data_hand[new_key] += 1
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                return [set_tiles[0] * 2, 'pair', str(number) * 2 + suit, status_set]
            elif (self.data_hand['is_chiitoi'] == True) and (self.wall_data.ALL_TILES[suit][tile] > 3):
                self.wall_data.ALL_TILES[suit][tile] -= 2
                for key, values in self.wall_data.TILE_DATA['pair'].items():
                    if set_tiles[0] in values:
                        # if (set_tiles[0] == self.data_hand['prevailed_wind'] or set_tiles[0] == self.data_hand[
                        #     'your_wind']
                        #         or suit == 'dragon'):
                        #     self.data_hand['additional_fu'] += 2
                        new_key = key + '_pair'
                        self.data_hand[new_key] += 1
                        break
                if suit in ['wind', 'dragon']:
                    self.data_hand['honor_sets'] += 1
                else:
                    self.data_hand[suit + '_sets'] += 1
                return [set_tiles[0] * 2, 'pair', str(number) * 2 + suit, status_set]

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

    def __churenpoto_create(self):
        choice_suit = { 'souzu': ("🀐🀐🀐🀑🀒🀓🀔🀕🀖🀗🀘🀘🀘", '🀐🀑🀒🀓🀔🀕🀖🀗🀘'),
                        'manzu': ('🀇🀇🀇🀈🀉🀊🀋🀌🀍🀎🀏🀏🀏', "🀇🀈🀉🀊🀋🀌🀍🀎🀏"),
                        'pinzu': ('🀙🀙🀙🀚🀛🀜🀝🀞🀟🀠🀡🀡🀡', "🀙🀚🀛🀜🀝🀞🀟🀠🀡") }
        suit = random.choice(('souzu', 'manzu', 'pinzu'))
        hand = choice_suit[suit][0]
        winning_tile = random.choice(choice_suit[suit][1])
        ready_hand = "".join(sorted(hand + winning_tile))
        rip_off = random.choice(ready_hand)
        if rip_off == winning_tile:
            self.data_hand['win_tile'] = winning_tile
            self.data_hand["yaku"]['special']["churenpoto"] = True
            self.data_hand['pretty_hand'] = ready_hand
            self.data_hand["base_fu"] = 40
            self.data_hand["additional_fu"] = 40
            self.data_hand["base_han"] = 26
        else:
            self.data_hand['win_tile'] = rip_off
            self.data_hand["yaku"]['special']["churenpoto"] = True
            self.data_hand['pretty_hand'] = ready_hand
            self.data_hand["base_fu"] = 40
            self.data_hand["additional_fu"] = 40
            self.data_hand["base_han"] = 13
        for j in ready_hand:
            self.wall_data.ALL_TILES[suit][j] -= 1
        self.data_hand['suit_win_tile'] = suit

    def __kokushi_musou_create(self):
        almost_ready_hand = "🀐🀘🀇🀏🀙🀡🀄🀆🀅🀀🀁🀂🀃"
        winning_tile = random.choice(almost_ready_hand)
        ready_hand = "".join(sorted(almost_ready_hand + winning_tile))
        rip_off = random.choice(ready_hand)
        if rip_off == winning_tile:
            self.data_hand['win_tile'] = winning_tile
            self.data_hand["yaku"]['special']["kokushi_musou"] = True
            self.data_hand['pretty_hand'] = ready_hand
            self.data_hand["base_fu"] = 0
            self.data_hand["additional_fu"] = 0
            self.data_hand["base_han"] = 26
        else:
            self.data_hand['win_tile'] = rip_off
            self.data_hand["yaku"]['special']["kokushi_musou"] = True
            self.data_hand['pretty_hand'] = ready_hand
            self.data_hand["base_fu"] = 0
            self.data_hand["additional_fu"] = 0
            self.data_hand["base_han"] = 13
        for j in ready_hand:
            for suit, tiles in self.wall_data.TILES_DICT.items():
                if j == self.wall_data.ALL_TILES[suit]:
                    self.wall_data.ALL_TILES[suit] -= 1
        self.data_hand['suit_win_tile'] = 'manzu'

    def hand_creator(self):
        """Here is collected all chi, pon or pair sets to create a ready hand."""
        is_chiitoi = True if (random.randint(0, 100) <= 10) else False
        is_churenpoto = True if (random.randint(0, 42000) == 999) else False
        is_kokushi_musou = True if (random.randint(0, 30000) == 1000) else False
        self.data_hand = { "yaku": { 'special': { }, 'simple': { } }, "is_valid": False, "base_fu": 0,
                           "additional_fu": 0, "base_han": 0,
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
                           'your_wind': random.choice(self.wall_data.TILES_DICT["wind"][::]), "is_chiitoi": False }
        if is_churenpoto:
            self.__churenpoto_create()
            self.data_hand["hand"] = []
        elif is_kokushi_musou:
            self.__kokushi_musou_create()
            self.data_hand["hand"] = []
        elif is_chiitoi:
            self.__chiitoi_create()
            self.data_hand["base_fu"] = 25
            self.data_hand["base_han"] += 2
            self.data_hand["hand"] = self.your_hand
            self.data_hand["yaku"]['simple']["chiitoi"] = True
        else:
            for _ in range(4):
                pon_chance = True if (random.randint(0, 100) <= 30) else False
                kan_chance = True if (random.randint(0, 100) <= 30) else False
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

    def build_dead_wall(self):
        number_right = 2 - (self.data_hand['kan_amount'] // 2)
        number_left = 4 - (self.data_hand['kan_amount'] // 2)
        wall = (self.wall_data.SPECIAL_TILE * number_left) + "".join(
            i[0] for i in self.data_hand['dora_pointers']['dora_pointers']) + (
                       self.wall_data.SPECIAL_TILE * number_right)
        return wall

    def build_hand(self):
        opened_sets = ''
        winning_set = ''
        closed_sets = ''
        for i, tile_set in enumerate(self.data_hand['hand']):
            if ("-" in tile_set[0]) or (self.wall_data.SPECIAL_TILE in tile_set[0]):
                opened_sets += tile_set[0]
            elif not winning_set and self.data_hand['win_tile'] in tile_set[0]:
                winning_set += tile_set[0]
            else:
                closed_sets += tile_set[0]
        x = self.data_hand['win_set'] + "".join(sorted(closed_sets)) + " " + opened_sets + "  " + self.data_hand[
            'win_tile']
        # x = sorted([i[0] for i in sorted(self.data_hand['hand'], key=lambda x: x[3] == 'closed')])
        # print(x)
        return x

    def get_data_hand(self):
        return self.data_hand

    def get_your_hand(self):
        return self.your_hand

    def get_wall(self):
        return self.wall_data

    def get_simple_hand(self):
        return f"""
       Hand: {self.data_hand['pretty_hand']}
       Dead wall: {self.data_hand['pretty_dead_wall']}
       Dora: {self.data_hand['dora']}, Dora Amount: {self.data_hand['dora_amount']}
       Han: {self.data_hand['base_han'] + self.data_hand['dora_amount']}
       Fu: {self.data_hand['rounded_fu']}
       Cost: {self.data_hand['score']}
       Yaku list: {self.data_hand['yaku']['simple'], self.data_hand['yaku']['special']}
       Win by: {"Tsumo" if self.data_hand['tsumo'] else "Ron"}
       {"You are dealer" if self.data_hand['your_wind'] == "🀀" else "You are non-dealer"}
       Winds: Prevailed {self.data_hand['prevailed_wind']}, Seat {self.data_hand['your_wind']}
       Win tile: {self.data_hand['win_tile']}
       {"Open" if self.data_hand['is_open'] else "Closed"} hand.
       Is valid: {self.data_hand['is_valid']}
       """
