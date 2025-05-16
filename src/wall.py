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

    COSTS = {
        'player': {
            1: {
                30: { 'tsumo':
                          (500, 300),
                      'ron':
                          1000,
                      },
                40: { 'tsumo':
                          (700, 400),
                      'ron':
                          1300,
                      },
                50: { 'tsumo':
                          (800, 400),
                      'ron':
                          1600,
                      },
                60: { 'tsumo':
                          (1000, 500),
                      'ron':
                          2000,
                      },
                70: { 'tsumo':
                          (1200, 600),
                      'ron':
                          2300,
                      },
                80: { 'tsumo':
                          (1300, 700),
                      'ron':
                          2600,
                      },
                90: { 'tsumo':
                          (1500, 800),
                      'ron':
                          2900,
                      },
                100: { 'tsumo':
                           (1600, 800),
                       'ron':
                           3200,
                       },
                110: { 'tsumo':
                           (1800, 900),
                       'ron':
                           3600,
                       },
            },
            2: {
                20: { 'tsumo':
                          (700, 400),
                      'ron':
                          1300,
                      },
                25: {
                    'ron':
                        1600,
                },
                30: { 'tsumo':
                          (1000, 500),
                      'ron':
                          2000,
                      },
                40: { 'tsumo':
                          (1300, 700),
                      'ron':
                          2600,
                      },
                50: { 'tsumo':
                          (1600, 800),
                      'ron':
                          3200,
                      },
                60: { 'tsumo':
                          (2000, 1000),
                      'ron':
                          3900,
                      },
                70: { 'tsumo':
                          (2300, 1200),
                      'ron':
                          4500,
                      },
                80: { 'tsumo':
                          (2600, 1300),
                      'ron':
                          5200,
                      },
                90: { 'tsumo':
                          (2900, 1500),
                      'ron':
                          5800,
                      },
                100: { 'tsumo':
                           (3200, 1600),
                       'ron':
                           6400,
                       },
                110: { 'tsumo':
                           (3600, 1800),
                       'ron':
                           7100,
                       },

            },
            3: {
                20: { 'tsumo':
                          (1300, 700),
                      'ron':
                          2600,
                      },
                25: { 'tsumo':
                          (1600, 800),
                      'ron':
                          3200,
                      },
                30: { 'tsumo':
                          (2000, 1000),
                      'ron':
                          3900,
                      },
                40: { 'tsumo':
                          (2600, 1300),
                      'ron':
                          5200,
                      },
                50: { 'tsumo':
                          (3200, 1600),
                      'ron':
                          6400,
                      },
                60: { 'tsumo':
                          (3900, 2000),
                      'ron':
                          7700,
                      },
                70: { 'tsumo':
                          (4000, 2000),
                      'ron':
                          8000,
                      },

            },
            4: {
                20: { 'tsumo':
                          (2600, 1300),
                      'ron':
                          5200,
                      },
                25: { 'tsumo':
                          (3200, 1600),
                      'ron':
                          6400,
                      },
                30: { 'tsumo':
                          (3900, 2000),
                      'ron':
                          7700,
                      }
            },
            5: {
                0: { 'tsumo':
                         (4000, 2000),
                     'ron':
                         8000,
                     },

            },
            6: {
                0: { 'tsumo':
                         (6000, 3000),
                     'ron':
                         12000,
                     },

            },
            7: {
                0: { 'tsumo':
                         (6000, 3000),
                     'ron':
                         12000,
                     },

            },
            8: {
                0: { 'tsumo':
                         (8000, 4000),
                     'ron':
                         16000,
                     },

            },
            9: {
                0: { 'tsumo':
                         (8000, 4000),
                     'ron':
                         16000,
                     },

            },
            10: {
                0: { 'tsumo':
                         (8000, 4000),
                     'ron':
                         16000,
                     },

            },
            11: {
                0: { 'tsumo':
                         (12000, 6000),
                     'ron':
                         24000,
                     },

            },
            12: {
                0: { 'tsumo':
                         (12000, 6000),
                     'ron':
                         24000,
                     },

            },
            # 13: {
            #     0: { 'tsumo':
            #              (16000, 8000),
            #          'ron':
            #              32000,
            #          },
            #
            # },
            # 26: {
            #     0: { 'tsumo':
            #              (32000, 16000),
            #          'ron':
            #              64000,
            #          },
            #
            # },
            # 39: {
            #     0: { 'tsumo':
            #              (48000, 24000),
            #          'ron':
            #              96000,
            #          },
            #
            # },
        },
        'dealer': {
            1: {
                30: { 'tsumo':
                          500,
                      'ron':
                          1500,
                      },
                40: { 'tsumo':
                          700,
                      'ron':
                          2000,
                      },
                50: { 'tsumo':
                          800,
                      'ron':
                          2400,
                      },
                60: { 'tsumo':
                          1000,
                      'ron':
                          2900,
                      },
                70: { 'tsumo':
                          1200,
                      'ron':
                          3400,
                      },
                80: { 'tsumo':
                          1300,
                      'ron':
                          3900,
                      },
                90: { 'tsumo':
                          1500,
                      'ron':
                          4400,
                      },
                100: { 'tsumo':
                           1600,
                       'ron':
                           4800,
                       },
                110: { 'tsumo':
                           1800,
                       'ron':
                           5300,
                       },
            },
            2: {
                20: { 'tsumo':
                          700,
                      'ron':
                          2000,
                      },
                25: {
                    'ron':
                        2400,
                },
                30: { 'tsumo':
                          1000,
                      'ron':
                          2900,
                      },
                40: { 'tsumo':
                          1300,
                      'ron':
                          3900,
                      },
                50: { 'tsumo':
                          1600,
                      'ron':
                          4800,
                      },
                60: { 'tsumo':
                          2000,
                      'ron':
                          5800,
                      },
                70: { 'tsumo':
                          2300,
                      'ron':
                          6800,
                      },
                80: { 'tsumo':
                          2600,
                      'ron':
                          7700,
                      },
                90: { 'tsumo':
                          2900,
                      'ron':
                          8700,
                      },
                100: { 'tsumo':
                           3200,
                       'ron':
                           9600,
                       },
                110: { 'tsumo':
                           3600,
                       'ron':
                           10600,
                       },

            },
            3: {
                20: { 'tsumo':
                          1300,
                      'ron':
                          3900,
                      },
                25: { 'tsumo':
                          1600,
                      'ron':
                          4800,
                      },
                30: { 'tsumo':
                          2000,
                      'ron':
                          5800,
                      },
                40: { 'tsumo':
                          2600,
                      'ron':
                          7700,
                      },
                50: { 'tsumo':
                          3200,
                      'ron':
                          9600,
                      },
                60: { 'tsumo':
                          3900,
                      'ron':
                          11600,
                      },

            },
            4: {
                20: { 'tsumo':
                          2600,
                      'ron':
                          7700,
                      },
                25: { 'tsumo':
                          3200,
                      'ron':
                          9600,
                      },
                30: { 'tsumo':
                          3900,
                      'ron':
                          11600,
                      }
            },
            5: {
                0: { 'tsumo':
                         4000,
                     'ron':
                         12000,
                     },

            },
            6: {
                0: { 'tsumo':
                         6000,
                     'ron':
                         18000,
                     },

            },
            7: {
                0: { 'tsumo':
                         6000,
                     'ron':
                         18000,
                     },

            },
            8: {
                0: { 'tsumo':
                         8000,
                     'ron':
                         24000,
                     },

            },
            9: {
                0: { 'tsumo':
                         8000,
                     'ron':
                         24000,
                     },

            },
            10: {
                0: { 'tsumo':
                         8000,
                     'ron':
                         24000,
                     },

            },
            11: {
                0: { 'tsumo':
                         12000,
                     'ron':
                         36000,
                     },

            },
            12: {
                0: { 'tsumo':
                         12000,
                     'ron':
                         36000,
                     },

            },
            # 13: {
            #     0: { 'tsumo':
            #              16000,
            #          'ron':
            #              48000,
            #          },
            #
            # },
            # 26: {
            #     0: { 'tsumo':
            #              32000,
            #          'ron':
            #              96000,
            #          },
            #
            # },
            # 39: {
            #     0: { 'tsumo':
            #              48000,
            #          'ron':
            #              144000,
            #          },
            #
            # },
        },
    }

    YAKUMAN_EXTENDER_DEALER = {
        (('tsumo', 16000), ('ron', 48000)): [i for i in range(13, 26)],
        (('tsumo', 32000), ('ron', 96000)): [i for i in range(26, 39)],
        (('tsumo', 48000), ('ron', 144000)): [i for i in range(39, 52)],
    }
    YAKUMAN_EXTENDER_PLAYER = {
        (('tsumo', (16000, 8000)), ('ron', 32000)): [i for i in range(13, 26)],
        (('tsumo', 32000, 16000), ('ron', 64000)): [i for i in range(26, 39)],
        (('tsumo', 48000, 24000), ('ron', 96000)): [i for i in range(39, 52)],
    }

    YAKUMAN_EXTENDER_REVERSED_DEALER = { v: { 0: { k[0][0]: k[0][1], k[1][0]: k[1][1] } }
                                         for k, li in YAKUMAN_EXTENDER_DEALER.items()
                                         for v in li }
    YAKUMAN_EXTENDER_REVERSED_PLAYER = { v: { 0: { k[0][0]: k[0][1], k[1][0]: k[1][1] } }
                                         for k, li in YAKUMAN_EXTENDER_PLAYER.items()
                                         for v in li }
    COSTS['dealer'].update(YAKUMAN_EXTENDER_REVERSED_DEALER)
    COSTS['player'].update(YAKUMAN_EXTENDER_REVERSED_PLAYER)
    WINNING_BY = {
        "pon": "syanpon",
        "chi": ["ryanmen", "kanchan", "penchan"],
        "pair": "tanki"
    }

    FORMS = {
        "ryanmen": (0, 2),
        "kanchan": 2,
        "penchan": 1,
        "syanpon": 9
    }

    FU_SPECIAL_SET = ['🀇', '🀏', '🀙', '🀡', '🀐', '🀘', "🀀", "🀁", "🀂", "🀃", "🀄", "🀅", "🀆"]
    FU_SPECIAL_PAIR = ["🀀", "🀁", "🀂", "🀃", "🀄", "🀅", "🀆"]

    FU_LIST_BY_SET = {
        "pon": { "special": 8, "usual": 4 },
        "pair": 2,
        "kan": { "special": 32, "usual": 16 },
    }
    BAD_WAIT = 2

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
            all_dora_pointer = { "doras":
                                     list(),
                                 "ura_doras":
                                     list() }
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
        return None

    # def pretty_wall(self, doras, kan_doras):
    #     "".join([tile for tile in range(7)])
