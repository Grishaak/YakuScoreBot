yaku_list = {
    "consecutive_yaku":
        {
            "pinfu": [
                "all_chi",
                "ron_from_chi",
                "rynamen"
            ],
            "ippeico":
                [
                    "consecutive_chi",
                ],
            "itsu": [
                "chi_suit"
            ],
            "sanshoko": [
                "indentical_chi_hand"
            ],
            "chanta": [
                "one_bordered_or_honor_tile_in_set"
            ],
            "djunchan": [
                "one_bordered_tile_in_set"
            ],
        },
    "pon_yaku": {
        "sanshoko_doko": [
            "three_concealed_sets"
        ],
        "toitoi": [
            "all_pons"
        ],
        "sananko": [
            "concealed_three_pons"
        ],
        "honroto": [
            "all_bordered_tiles"
        ]
    },
    "additional_yaku": {
        "yakuhai": [
            "honor_set"
        ],
        "tanyao": [
            "all_middle_tiles"
        ],
        "shosangen": [
            "two_dragons"
        ],
    },
    "one_suit_yaku": {
        "honitsu": [
            "half_suit_hand"
        ],
        "chinitsu": [
            "full_suit_hand"
        ],
    },
    "special_yaku": {
        "chiitoitsu": [
            "all_pairs",
        ]
    },

}


def find_ippeiko_or_ryanppeiko(a_hand: dict):
    if a_hand['is_open'] or a_hand['is_chiitoi']:
        pass
    else:
        hand = a_hand['hand'].copy()
        hand = sorted(hand, key=lambda x: x[0])
        hand = list(filter(lambda x: x[1] != 'pair', hand))
        # print(hand)
        if (hand[0] == hand[1]) and (hand[2] == hand[3]):
            a_hand['yaku']['ryanppeiko'] = True
            a_hand['base_han'] += 3
        elif hand[0] == hand[1] or hand[1] == hand[2] or hand[2] == hand[3]:
            a_hand['yaku']['ippeiko'] = True
            a_hand['base_han'] += 1


def find_sanshoko(a_hand: dict):
    hand = a_hand['hand'].copy()
    hand = sorted(hand, key=lambda x: x[2][0:3])
    # print(hand)
    hand = list(filter(lambda x: x[1] != 'pair', hand))
    if a_hand["identical_chi_in_diff_suits"] == 3:
        han = 2
        if a_hand['is_open']:
            han = -1
        a_hand['yaku']['sanshoko'] = True
        a_hand['base_han'] += han


def find_honroto_chonroto(a_hand: dict):
    if (not a_hand['is_chiitoi']) and ((a_hand["border_pons"] + a_hand['honor_sets']) == 4) and a_hand["border_pair"]:
        a_hand['yaku']['honroto'] = True
        han = 2
        a_hand['base_han'] += han


def find_toitoi(a_hand: dict):
    if a_hand['pon_amount'] + a_hand['kan_amount'] == 4:
        a_hand['yaku']['toitoi'] = True
        han = 2
        a_hand['base_han'] += han


def find_tanyao(a_hand: dict):
    if (not a_hand['border_pons'] and not a_hand["border_chis"]
            and not a_hand["wind_pons"] and not a_hand["dragon_pons"] and not a_hand['border_pair']
            and not a_hand['dragon_pair'] and not a_hand['wind_pair'] and not a_hand['border_kans']
            and not a_hand['wind_kans'] and not a_hand['dragon_kans']):
        a_hand['yaku']['tanyao'] = True
        han = 1
        a_hand['base_han'] += han


def find_yakuhai(a_hand: dict):
    if not a_hand['is_chiitoi']:
        han = 0
        for set_tiles in a_hand['hand']:
            if (a_hand['your_wind'] in set_tiles[0]) and len(set_tiles[0]) >= 3:
                han += 1
                a_hand['yaku']['yakuhai'] = True
            if (a_hand['prevailed_wind'] in set_tiles[0]) and len(set_tiles[0]) >= 3:
                han += 1
                a_hand['yaku']['yakuhai'] = True
        if a_hand['dragon_pons'] or a_hand['dragon_kans']:
            han = a_hand['dragon_pons'] + a_hand['dragon_kans'] + han
            a_hand['yaku']['yakuhai'] = True
        a_hand['base_han'] += han


def find_djunchan_or_chanta(a_hand: dict):
    if not a_hand['yaku'].get('honroto'):
        if ((a_hand["border_chis"] + a_hand["border_pons"]) == 4) and a_hand["border_pair"]:
            han = 3
            if a_hand['is_open']:
                han -= 1
            a_hand['yaku']['djunchan'] = True
            a_hand['base_han'] += han
        elif (not a_hand['yaku'].get('djunchan') and not a_hand['yaku'].get('honroto') and
              ((
                       a_hand["border_chis"] + a_hand["border_pons"] + a_hand["dragon_pons"] + a_hand[
                   "wind_pons"]) == 4)
              and (
                      a_hand["border_pair"] or a_hand["wind_pair"])):
            han = 3
            if a_hand['is_open']:
                han -= 1
            a_hand['yaku']['djunchan'] = True
            a_hand['base_han'] += han


def find_sesangen(a_hand: dict):
    if a_hand['dragon_pons'] == 2 and a_hand['dragon_pair']:
        han = 2
        a_hand['yaku']['sesangen'] = True
        a_hand['base_han'] += han


def find_sankatsu(a_hand: dict):
    if a_hand['kan_amount'] == 3:
        han = 2
        a_hand['yaku']['sankatsu'] = True
        a_hand['base_han'] += han


def find_ittsu(a_hand: dict):
    if a_hand['full_suit']:
        han = 2
        if a_hand['is_open']:
            han -= 1
        a_hand['yaku']['ittsu'] = True
        a_hand['base_han'] += han


def find_sandoko(a_hand: dict):
    if a_hand['identical_pons'] == 3:
        han = 2
        a_hand['yaku']['sandoko'] = True
        a_hand['base_han'] += han


def find_honitsu(a_hand: dict):
    han = 0
    if not a_hand['yaku'].get('chinitsu'):
        if not a_hand['is_chiitoi'] and (((a_hand['honor_sets'] + a_hand['manzu_sets']) >= 5) or (
                (a_hand['honor_sets'] + a_hand['souzu_sets']) >= 5) or (
                                                 (a_hand['honor_sets'] + a_hand['pinzu_sets']) >= 5) and a_hand[
                                             'honor_sets']):
            han = 3
            a_hand['yaku']['honitsu'] = True
            if a_hand['is_open']:
                han -= 1

        elif (a_hand['is_chiitoi'] and (((a_hand['dragon_pair'] + a_hand['wind_pair'] + a_hand['manzu_sets']) == 7) or
                                        ((a_hand['dragon_pair'] + a_hand['wind_pair'] + a_hand['manzu_sets']) == 7) or
                                        ((a_hand['dragon_pair'] + a_hand['wind_pair'] + a_hand['manzu_sets']) == 7)
        )):
            han = 3
            a_hand['yaku']['honitsu'] = True
            if a_hand['is_open']:
                han -= 1
    a_hand["base_han"] += han


def find_chinitsu(a_hand: dict):
    han = 0
    if not a_hand['yaku'].get('honitsu'):
        if not a_hand['is_chiitoi'] and ((a_hand['manzu_sets'] == 5) or (a_hand['souzu_sets'] == 5) or (
                a_hand['pinzu_sets'] == 5)):
            han = 6
            a_hand['yaku']['chinitsu'] = True
            if a_hand['is_open']:
                han -= 1
        elif (a_hand['is_chiitoi'] and ((a_hand['manzu_sets'] == 7) or
                                        (a_hand['souzu_sets'] == 7) or
                                        (a_hand['pinzu_sets'] == 7)
        )):
            han = 6
            a_hand['yaku']['chinitsu'] = True
            if a_hand['is_open']:
                han -= 1
    a_hand["base_han"] += han


def find_pinfu(a_hand: dict):
    if not a_hand['additional_fu']:
        a_hand['yaku']['pinfu'] += 1
        a_hand["base_han"] += 1
