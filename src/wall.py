import random
from pprint import pprint
from yaku_list import *


class Wall:
    TILES_DICT = {
        "wind": ["🀀", "🀁", "🀂", "🀃"],
        "dragon": ["🀄", "🀆", "🀅"],
        "manzu": ["🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏"],
        "pinzu": ["🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡"],
        "souzu": ["🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"],
    }
    SPECIAL_TILE = '🀫'
    RANGES = {
        "chi": {
            "manzu": range(7),
            "pinzu": range(7),
            "souzu": range(7)
        },
        "pon": {
            "wind": range(4),
            "dragon": range(3),
            "manzu": range(9),
            "pinzu": range(9),
            "souzu": range(9)
        }
    }
    SUITS = {
        'chi': ["manzu", "souzu", "pinzu"],
        'pon': ["manzu", "souzu", "pinzu", "dragon", "wind"]
    }

    TILE_DATA = {
        "kan": {
            "border": ['🀇', '🀏', '🀙', '🀡', '🀐', '🀘'],
            "wind": ["🀀", "🀁", "🀂", "🀃"],
            "dragon": ["🀄", "🀅", "🀆"]
        },
        "pon": {
            "border": ['🀇', '🀏', '🀙', '🀡', '🀐', '🀘'],
            "wind": ["🀀", "🀁", "🀂", "🀃"],
            "dragon": ["🀄", "🀅", "🀆"]
        },
        "chi": {
            "border": ['🀇', '🀏', '🀙', '🀡', '🀐', '🀘']
        },
        "pair": {
            "border": ['🀇', '🀏', '🀙', '🀡', '🀐', '🀘'],
            "wind": ["🀀", "🀁", "🀂", "🀃"],
            "dragon": ["🀄", "🀅", "🀆"]
        },
    }

    COSTS = (
        {"mangan": {"han": 3, "fu": 70}},
        {"mangan": {"han": 4, "fu": 40}},
        {"mangan": {"han": 5, "fu": 0}},
        {"haneman": {"han": 6, "fu": 0}},
        {"haneman": {"han": 7, "fu": 0}},
        {"baiman": {"han": 8, "fu": 0}},
        {"baiman": {"han": 9, "fu": 0}},
        {"baiman": {"han": 10, "fu": 0}},
        {"sanbaiman": {"han": 11, "fu": 0}},
        {"sanbaiman": {"han": 12, "fu": 0}},
        {"yakuman": {"han": 13, "fu": 0}},
    )

    def __init__(self):
        self.ALL_TILES = dict()
        self.DEAD_WALL = list()
        self.__create_tiles()

    #
    def __create_tiles(self):
        for suit, tiles in self.TILES_DICT.items():
            new_dict = dict()
            for tile in tiles:
                new_dict[tile] = 4
            self.ALL_TILES[suit] = new_dict
        self.__pick_dead_wall()

    def __pick_dead_wall(self):
        walls = []
        for suit, tiles in self.TILES_DICT.items():
            for i in tiles:
                for _ in range(4):
                    walls.append((i, suit))
        for _ in range(14):
            dead_tile = random.choice(walls)
            self.DEAD_WALL.append(dead_tile)
        for tile in self.DEAD_WALL:
            for suit, set_suit in self.ALL_TILES.items():
                for i in set_suit.keys():
                    if tile[0] == i:
                        self.ALL_TILES[suit][tile[0]] -= 1

    def choose_random_suit(self, data_set):
        """Choose a random suit for a set (pon) or a consecutive tiles (chi)"""
        return random.choice(self.SUITS[data_set])

    def choose_random_number(self, suit, data_set):
        """Choose a random number for a set (pon) or a consecutive tiles (chi)"""
        return random.choice(self.RANGES[data_set][suit])

    def find_all_doras(self, p_d: tuple, p_ud: tuple, p_kd: list, p_kud: list):
        if self.DEAD_WALL:
            all_dora_pointer = {"doras":
                                    list(),
                                "ura_doras":
                                    list()}
            for set_dora in (p_d, *p_kd):
                dora_index = self.TILES_DICT[set_dora[1]].index(set_dora[0])
                if dora_index == len(self.TILES_DICT[set_dora[1]]) - 1:
                    dora = self.TILES_DICT[set_dora[1]][0]
                else:
                    dora = self.TILES_DICT[set_dora[1]][dora_index + 1]
                all_dora_pointer['doras'].append(dora)
            for set_dora in (p_ud, *p_kud):
                dora_index = self.TILES_DICT[set_dora[1]].index(set_dora[0])
                if dora_index == len(self.TILES_DICT[set_dora[1]]) - 1:
                    dora = self.TILES_DICT[set_dora[1]][0]
                else:
                    dora = self.TILES_DICT[set_dora[1]][dora_index + 1]
                all_dora_pointer['ura_doras'].append(dora)

            return all_dora_pointer

    def pretty_wall(self, doras, kan_doras):
        "".join([tile for tile in range(7)])
