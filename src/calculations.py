import random

from src.hand import Hand
from src.yaku_list import *


class CalculatedHand:

    def __init__(self, hand: Hand):
        self.a_hand = hand
        self.calculated_hand = hand.get_data_hand()
        self.wall_data = hand.get_wall()
        self.result_hand = self.__yaku_calculator()
        # print(self.calculated_hand, self.wall_data)

    def __count_fu(self):
        additional_fu = 0
        for set_tiles in self.calculated_hand['hand']:
            # print(set_tiles[1])
            if ((set_tiles[1] != 'pair') and (set_tiles[1] != 'chi')) and (
                    set_tiles[0][2] in self.wall_data.FU_SPECIAL_SET):
                # print(self.wall_data.FU_LIST_BY_SET.get(set_tiles[1], 0))
                add_fu = self.wall_data.FU_LIST_BY_SET.get(set_tiles[1], 0).get('special')
            elif (set_tiles[1] != 'pair') and (set_tiles[1] != 'chi'):
                add_fu = self.wall_data.FU_LIST_BY_SET.get(set_tiles[1], 0).get('usual')
            elif (set_tiles[1] == 'pair') and (set_tiles[0][0] in self.wall_data.FU_SPECIAL_PAIR):
                if ((set_tiles[0][0] == self.calculated_hand['prevailed_wind'])
                        or (set_tiles[0][0] == self.calculated_hand['your_wind'])):
                    add_fu = self.wall_data.FU_LIST_BY_SET.get("pair")
                elif set_tiles[0][0] in ["🀄", "🀅", "🀆"]:
                    add_fu = self.wall_data.FU_LIST_BY_SET.get("pair")
                else:
                    add_fu = 0
            else:
                add_fu = 0
            if (set_tiles[3] == 'opened') and add_fu:
                add_fu //= 2
            additional_fu += add_fu
        self.calculated_hand['additional_fu'] += additional_fu

    def __count_doras(self):
        for set_tile in self.calculated_hand['hand']:
            for tile in set_tile[0]:
                for dora in self.calculated_hand['dora']['doras']:
                    if tile == dora:
                        self.calculated_hand['dora_amount'] += 1
                if self.calculated_hand['yaku']['simple'].get('riichi'):
                    for ura_dora in self.calculated_hand['dora']['ura_doras']:
                        if tile == ura_dora:
                            self.calculated_hand['dora_amount'] += 1

    def __count_yakumans(self):
        if not self.calculated_hand['is_open']:
            find_suanko(self.calculated_hand)
            find_churenpoto(self.calculated_hand)
        find_sukatsu(self.calculated_hand)
        find_chonroto(self.calculated_hand)
        find_daisangen(self.calculated_hand)
        find_tsuiso(self.calculated_hand)
        find_sosushi_daishushi(self.calculated_hand)
        find_ruisou(self.calculated_hand)

    def __count_all_simple_yaku(self):

        if not self.calculated_hand['is_open']:
            find_ippeiko_or_ryanppeiko(self.calculated_hand)
            find_pinfu(self.calculated_hand)

        find_yakuhai(self.calculated_hand)
        find_tanyao(self.calculated_hand)
        find_ittsu(self.calculated_hand)
        find_honroto(self.calculated_hand)
        find_djunchan_or_chanta(self.calculated_hand)
        find_honitsu_chinitsu(self.calculated_hand)
        find_sanshoko_sandoko(self.calculated_hand)
        find_toitoi(self.calculated_hand)
        find_sesangen(self.calculated_hand)
        find_sankatsu(self.calculated_hand)
        find_sananko(self.calculated_hand)

    def __count_all_yaku(self):
        self.__count_yakumans()
        if not self.calculated_hand['yaku']['special']:
            self.__count_all_simple_yaku()
        if self.calculated_hand["yaku"]['simple'] or self.calculated_hand["yaku"]['special']:
            self.calculated_hand["is_valid"] = True
        else:
            self.calculated_hand["is_valid"] = False

    def __win_by(self):
        set_of_tile = random.choice(self.calculated_hand['hand'])
        winning_set, which_set, suit, status = set_of_tile[0], set_of_tile[1], set_of_tile[2], set_of_tile[3]
        while (which_set == 'kan') or (status == 'opened'):
            set_of_tile = random.choice(self.calculated_hand['hand'])
            winning_set, which_set, suit, status = set_of_tile[0], set_of_tile[1], set_of_tile[2], set_of_tile[3]
        indexed = self.calculated_hand['hand'].index(set_of_tile)
        wait_tile = random.choice(winning_set)
        tile_index = winning_set.index(wait_tile)
        if which_set == 'chi':
            win_set = winning_set.replace(wait_tile, '')
            if (tile_index == 2 and winning_set[0] in ("🀇", "🀙", "🀐")) \
                    or (tile_index == 0 and winning_set[2] in ("🀏", "🀡", "🀘")):
                wait = self.wall_data.WINNING_BY[which_set][2]
            elif tile_index == 1:
                wait = self.wall_data.WINNING_BY[which_set][1]
            else:
                wait = self.wall_data.WINNING_BY[which_set][0]
            if wait == 'ryanmen':
                self.calculated_hand['bad_wait'] = False
            else:
                self.calculated_hand['bad_wait'] = True
        elif which_set == 'pon':
            win_set = winning_set[:2]
            if self.calculated_hand['ron']:
                self.calculated_hand['hand'][indexed][3] = 'opened'
                self.calculated_hand['opened_pons'] += 1
            self.calculated_hand['bad_wait'] = True
            wait = self.wall_data.WINNING_BY[which_set]
        else:
            win_set = winning_set[0]
            self.calculated_hand['bad_wait'] = True
            wait = self.wall_data.WINNING_BY[which_set]
        if self.calculated_hand.get('bad_wait'):
            self.calculated_hand['additional_fu'] += 2
        self.calculated_hand['win_set'] = win_set
        self.calculated_hand['win_tile'] = wait_tile
        self.calculated_hand['suit_win_tile'] = "".join([i for i in suit if not i.isdigit()])
        self.calculated_hand['wait'] = wait

    def __scoring(self):
        all_hans = self.calculated_hand['base_han'] + self.calculated_hand['dora_amount']
        rounded_fu = self.calculated_hand['base_fu'] + self.calculated_hand['additional_fu']
        if not self.calculated_hand['is_chiitoi']:
            rounded_fu += ((10 - (rounded_fu % 10)) if (rounded_fu % 10) != 0 else 0)
        self.calculated_hand['rounded_fu'] = rounded_fu
        if all_hans >= 5:
            rounded_fu = 0
        elif (all_hans == 4 and rounded_fu > 30) or (all_hans == 3 and rounded_fu > 60):
            rounded_fu = 0
            all_hans = 5
        # print(
        #     f"All hans: {all_hans}, Rounded fu: {rounded_fu}, {self.calculated_hand['yaku']}, {self.wall_data.COSTS.get(all_hans)}")
        if self.calculated_hand['your_wind'] == "🀀":
            if self.calculated_hand['tsumo']:
                score = self.wall_data.COSTS['dealer'].get(all_hans).get(rounded_fu).get('tsumo')
                score = f"{score}/{score}"
            else:
                score = self.wall_data.COSTS['dealer'].get(all_hans).get(rounded_fu).get('ron')
        else:
            if self.calculated_hand['tsumo']:
                score = self.wall_data.COSTS['player'].get(all_hans).get(rounded_fu).get('tsumo')
                score = f"{score[0]}/{score[1]}"
            else:
                score = self.wall_data.COSTS['player'].get(all_hans).get(rounded_fu).get('ron')
        return str(score)

    def __yaku_calculator(self):
        # if self.calculated_hand['yaku']['special'].get('churenpoto'):
        #     print('Chuuren')
        # elif self.calculated_hand['yaku']['special'].get('kokushi_musou'):
        #     print('kokushi')
        riichi_chance = True if random.randint(0, 100) <= 45 else False
        ippatsu_chance = True if random.randint(0, 100) <= 25 else False
        tsumo_chance = True if random.randint(0, 100) >= 35 else False
        hoitei_haitei_chance = True if random.randint(0, 100) <= 5 else False
        robbing_kan = True if random.randint(0, 100) <= 25 else False
        after_kan = True if random.randint(0, 100) <= 25 else False
        pointer_dora = self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
        pointer_ura_dora = self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
        pointer_kan_dora = [self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
                            for i in range(self.calculated_hand['kan_amount'])]
        pointer_kan_ura_dora = [self.wall_data.DEAD_WALL.pop(random.randrange(len(self.wall_data.DEAD_WALL)))
                                for i in range(self.calculated_hand['kan_amount'])]
        doras = self.wall_data.find_all_doras(pointer_dora, pointer_ura_dora, pointer_kan_dora,
                                              pointer_kan_ura_dora)

        self.calculated_hand['dora_pointers'] = { 'dora_pointers': [pointer_dora, *pointer_kan_dora],
                                                  'ura_dora_pointers': [pointer_ura_dora, *pointer_kan_ura_dora] }
        if riichi_chance and not self.calculated_hand['is_open']:
            self.calculated_hand['yaku']['simple']['riichi'] = True
            self.calculated_hand['base_han'] += 1
            if ippatsu_chance:
                self.calculated_hand['yaku']['simple']['ippatsu'] = True
                self.calculated_hand['base_han'] += 1

        if tsumo_chance:
            if not self.calculated_hand['is_open']:
                self.calculated_hand['yaku']['simple']['menzen_tsumo'] = True
                self.calculated_hand['base_han'] += 1
            self.calculated_hand['base_fu'] = 20
            self.calculated_hand['tsumo'] = True
        else:
            self.calculated_hand['base_fu'] = 20
            if not self.calculated_hand['is_open']:
                self.calculated_hand['base_fu'] += 10
            self.calculated_hand['ron'] = True
            # if not self.calculated_hand['yaku'].get('ippatsu') and robbing_kan \
            #         and self.wall_data.ALL_TILES[self.calculated_hand['suit_win_tile']][self.calculated_hand['win_tile']] > 2:
            #     self.calculated_hand['yaku']['after_kan'] = True
            #     self.calculated_hand['base_han'] += 1
        if ((not self.calculated_hand['yaku']['special'].get('churenpoto')) and
                (not self.calculated_hand['yaku']['special'].get('kokushi_musou'))):
            self.__win_by()
            self.__count_fu()

        if (self.calculated_hand['tsumo'] and self.calculated_hand['kan_amount'] and
                (not self.calculated_hand['yaku']['simple']
                        .get('ippatsu')) and after_kan and (
                        self.calculated_hand['win_tile'] in [i[0] for i in self.wall_data.DEAD_WALL])):
            self.calculated_hand['yaku']['simple']['after_kan'] = True
            self.calculated_hand['base_han'] += 1
        elif (self.calculated_hand['ron'] and not self.calculated_hand['yaku']['simple'].get('ippatsu')
              and robbing_kan and self.wall_data.ALL_TILES[self.calculated_hand['suit_win_tile']]
                      .get(self.calculated_hand['win_tile'], 0) > 2):
            self.calculated_hand['yaku']['simple']['robbing_kan'] = True
            self.calculated_hand['base_han'] += 1
        # Checking the chance for last draw winning tile or ron on last discard.
        if hoitei_haitei_chance:
            self.calculated_hand['yaku']['simple']['hotei'] = True
            self.calculated_hand['base_han'] += 1
        if self.calculated_hand['yaku']['special']:
            for i in self.calculated_hand['yaku']['special']:
                self.calculated_hand['base_han'] += 1
        if (self.calculated_hand['yaku']['special'].get('churenpoto')
                or self.calculated_hand['yaku']['special'].get('kokushi_musou')):
            self.calculated_hand['pretty_dead_wall'] = self.a_hand.build_dead_wall()
            return self.calculated_hand
        else:
            self.__count_all_yaku()
            if self.calculated_hand['is_valid']:
                if (not self.calculated_hand['yaku']['simple'].get('pinfu')) and self.calculated_hand['tsumo']:
                    self.calculated_hand['additional_fu'] += 2
                elif (not self.calculated_hand['additional_fu'] and self.calculated_hand['ron']
                      and not self.calculated_hand['yaku']['simple'].get('pinfu')):
                    self.calculated_hand['additional_fu'] += 2

                if self.calculated_hand['is_chiitoi']:
                    self.calculated_hand['additional_fu'] = 0
                    self.calculated_hand['base_fu'] = 25
                self.calculated_hand['dora'] = doras
                self.__count_doras()

                self.calculated_hand['pretty_dead_wall'] = self.a_hand.build_dead_wall()
                self.calculated_hand['pretty_hand'] = self.a_hand.build_hand()
                self.calculated_hand['score'] = self.__scoring()
            return self.calculated_hand

    def get_result_hand(self):
        return self.result_hand
