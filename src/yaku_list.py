simple_yaku_list = ['pinfu', 'ippeiko', 'honroto', 'chanta', 'djunchan',
                    'toitoi', 'tanyao', 'yakuhai', 'ittsu', 'chiitoi',
                    'sanshoko', 'chinitsu', 'honitsu',
                    ]
hard_yaku_list = ['sesangen', 'sankatsu', 'sananko', 'after_kan', 'robbing_kan', 'sandoko', 'ryanppeiko']

yakuman_yaku_list = [
    'suanko', 'sukatsu', 'chonroto', 'daisangen',
    'sosushi', 'daisushi', 'tsuiso',
    'churenpoto',
    'ruisou',
    # 'tenhou', 'chihou',
    'kokushi_musou',
]

ittsu_samples = ["🀇🀈🀉🀊🀋🀌🀍🀎🀏",
                 "🀙🀚🀛🀜🀝🀞🀟🀠🀡",
                 "🀐🀑🀒🀓🀔🀕🀖🀗🀘"]

churenpoto_samples = {
    "manzu": ["🀇🀇🀇🀇🀈🀉🀊🀋🀌🀍🀎🀏🀏🀏", "🀇🀇🀇🀈🀈🀉🀊🀋🀌🀍🀎🀏🀏🀏", "🀇🀇🀇🀈🀉🀉🀊🀋🀌🀍🀎🀏🀏🀏",
              "🀇🀇🀇🀈🀉🀊🀋🀋🀌🀍🀎🀏🀏🀏", "🀇🀇🀇🀈🀉🀊🀋🀌🀌🀍🀎🀏🀏🀏", "🀇🀇🀇🀈🀉🀊🀋🀌🀍🀍🀎🀏🀏🀏",
              "🀇🀇🀇🀈🀉🀊🀊🀋🀌🀍🀎🀏🀏🀏", "🀇🀇🀇🀈🀉🀊🀋🀌🀍🀎🀎🀏🀏🀏", "🀇🀇🀇🀈🀉🀊🀋🀌🀍🀎🀏🀏🀏🀏", ],
    "pinzu": ["🀙🀙🀙🀙🀚🀛🀜🀝🀞🀟🀠🀡🀡🀡", "🀙🀙🀙🀚🀚🀛🀜🀝🀞🀟🀠🀡🀡🀡", "🀙🀙🀙🀚🀛🀛🀜🀝🀞🀟🀠🀡🀡🀡",
              "🀙🀙🀙🀚🀛🀜🀜🀝🀞🀟🀠🀡🀡🀡", "🀙🀙🀙🀚🀛🀜🀝🀝🀞🀟🀠🀡🀡🀡", "🀙🀙🀙🀚🀛🀜🀝🀞🀞🀟🀠🀡🀡🀡",
              "🀙🀙🀙🀚🀛🀜🀝🀞🀟🀟🀠🀡🀡🀡", "🀙🀙🀙🀚🀛🀜🀝🀞🀟🀠🀠🀡🀡🀡", "🀙🀙🀙🀚🀛🀜🀝🀞🀟🀠🀡🀡🀡🀡", ],
    "souzu": ["🀐🀐🀐🀐🀑🀒🀓🀔🀕🀖🀗🀘🀘🀘", "🀐🀐🀐🀑🀑🀒🀓🀔🀕🀖🀗🀘🀘🀘", "🀐🀐🀐🀑🀒🀒🀓🀔🀕🀖🀗🀘🀘🀘",
              "🀐🀐🀐🀑🀒🀓🀓🀔🀕🀖🀗🀘🀘🀘", "🀐🀐🀐🀑🀒🀓🀔🀔🀕🀖🀗🀘🀘🀘", "🀐🀐🀐🀑🀒🀓🀔🀕🀕🀖🀗🀘🀘🀘",
              "🀐🀐🀐🀑🀒🀓🀔🀕🀖🀖🀗🀘🀘🀘", "🀐🀐🀐🀑🀒🀓🀔🀕🀖🀗🀗🀘🀘🀘", "🀐🀐🀐🀑🀒🀓🀔🀕🀖🀗🀘🀘🀘🀘"]
}


####-------------------------------------Simple Yaku finders-----------------------------------------------------


def find_ippeiko_or_ryanppeiko(a_hand: dict):
    if a_hand['is_open'] or a_hand['is_chiitoi']:
        pass
    else:
        hand = a_hand['hand'].copy()
        hand = sorted(hand, key=lambda x: x[0])
        hand = list(filter(lambda x: x[1] != 'pair', hand))
        if (hand[0] == hand[1]) and (hand[2] == hand[3]):
            a_hand['yaku']['simple']['ryanppeiko'] = True
            a_hand['base_han'] += 3
        elif hand[0] == hand[1] or hand[1] == hand[2] or hand[2] == hand[3]:
            a_hand['yaku']['simple']['ippeiko'] = True
            a_hand['base_han'] += 1


def find_sanshoko_sandoko(a_hand: dict):
    coincidence_dict = { }
    hand = a_hand['hand'].copy()
    hand = sorted(hand, key=lambda x: x[2][0:3])
    hand_chi = list(sorted(filter(lambda x: x[1] == 'chi', hand), key=lambda x: x[0][:3]))
    hand_pon = list(sorted(filter(
        lambda x: (x[1] in ('pon', 'kan')) and (f"{x[2][4:] if x[1] == 'kan' else x[2][3:]}" not in ['dragon', 'wind']),
        hand), key=lambda x: x[0][:3]))
    flag = False
    if len(hand_chi) >= 3:
        flag = True
    if flag:
        hand = hand_chi
    else:
        hand = hand_pon
    for i in hand:
        if not coincidence_dict.get(i[2][:3]):
            coincidence_dict[i[2][:3]] = dict()
            if i[1] == 'kan':
                coincidence_dict[i[2][:3]][i[2][4:]] = True
            else:
                coincidence_dict[i[2][:3]][i[2][3:]] = True
        else:
            if i[1] == 'kan':
                coincidence_dict[i[2][:3]][i[2][4:]] = True
            else:
                coincidence_dict[i[2][:3]][i[2][3:]] = True
    for j in coincidence_dict.values():
        if len(j) == 3:
            han = 2
            if a_hand['is_open'] and flag:
                han -= 1
            if flag:
                a_hand['yaku']['simple']['sanshoko'] = True
                a_hand['base_han'] += han
            else:
                a_hand['yaku']['simple']['sandoko'] = True
                a_hand['base_han'] += han
            break


def find_honroto(a_hand: dict):
    if a_hand['is_chiitoi']:
        if a_hand["border_pair"] and ((a_hand["border_pair"] + a_hand['honor_sets']) == 7):
            a_hand['yaku']['simple']['honroto'] = True
            han = 2
            a_hand['base_han'] += han
    else:
        if a_hand['honor_sets'] and (((a_hand["border_pons"] + a_hand['honor_sets']) == 4) and a_hand["border_pair"]):
            a_hand['yaku']['simple']['honroto'] = True
            han = 2
            a_hand['base_han'] += han


def find_toitoi(a_hand: dict):
    if (a_hand['pon_amount'] + a_hand['kan_amount']) == 4:
        a_hand['yaku']['simple']['toitoi'] = True
        han = 2
        a_hand['base_han'] += han


def find_tanyao(a_hand: dict):
    if (not a_hand['border_pons'] and not a_hand["border_chis"]
            and not a_hand["wind_pons"] and not a_hand["dragon_pons"] and not a_hand['border_pair']
            and not a_hand['dragon_pair'] and not a_hand['wind_pair'] and not a_hand['border_kans']
            and not a_hand['wind_kans'] and not a_hand['dragon_kans']):
        a_hand['yaku']['simple']['tanyao'] = True
        han = 1
        a_hand['base_han'] += han


def find_yakuhai(a_hand: dict):
    if not a_hand['is_chiitoi']:
        han = 0
        for set_tiles in a_hand['hand']:
            if (a_hand['your_wind'] in set_tiles[0]) and len(set_tiles[0]) >= 3:
                han += 1
                a_hand['yaku']['simple']['yakuhai'] = True
            if (a_hand['prevailed_wind'] in set_tiles[0]) and len(set_tiles[0]) >= 3:
                han += 1
                a_hand['yaku']['simple']['yakuhai'] = True
        if a_hand['dragon_pons'] or a_hand['dragon_kans']:
            han += a_hand['dragon_pons'] + a_hand['dragon_kans']
            a_hand['yaku']['simple']['yakuhai'] = True
        # print(f'Yakuhai han: {han}')
        a_hand['base_han'] += han


def find_djunchan_or_chanta(a_hand: dict):
    if not a_hand['yaku']['simple'].get('honroto'):
        if (a_hand["border_chis"] and (
                (a_hand["border_chis"] + a_hand["border_pons"]) == 4) and a_hand["border_pair"]):
            han = 3
            if a_hand['is_open']:
                han -= 1
            a_hand['yaku']['simple']['djunchan'] = True
            a_hand['base_han'] += han
        elif (a_hand["border_chis"] and a_hand["honor_sets"]) and (
                ((a_hand["border_chis"] + a_hand["border_pons"] + a_hand["dragon_pons"] + a_hand["wind_pons"]) == 4)
                and (a_hand["border_pair"] or a_hand["wind_pair"] or a_hand["dragon_pair"])):
            han = 2
            if a_hand['is_open']:
                han -= 1
            a_hand['yaku']['simple']['chanta'] = True
            a_hand['base_han'] += han


def find_ittsu(a_hand: dict):
    han = 2
    hand = a_hand['hand'].copy()
    hand = "".join(sorted("".join([i[0] for i in filter(lambda x: (x[1] != 'pair') or (x[0] == '-'), hand)])
                          .replace('-', ''), key=lambda x: x[0]))
    if hand[:9] in ittsu_samples:
        a_hand['yaku']['simple']['ittsu'] = True
        a_hand['base_han'] += han
        if a_hand['is_open']:
            a_hand['base_han'] -= 1


def find_honitsu_chinitsu(a_hand: dict):
    han = 0
    if a_hand['is_chiitoi']:
        if (((a_hand['dragon_pair'] + a_hand['wind_pair'] + a_hand['manzu_sets']) == 7) or
                ((a_hand['dragon_pair'] + a_hand['wind_pair'] + a_hand['manzu_sets']) == 7) or
                ((a_hand['dragon_pair'] + a_hand['wind_pair'] + a_hand['manzu_sets']) == 7)
        ):
            han = 3
            a_hand['yaku']['simple']['honitsu'] = True
        elif ((a_hand['manzu_sets'] == 7) or
              (a_hand['souzu_sets'] == 7) or
              (a_hand['pinzu_sets'] == 7)
        ):
            han = 6
            a_hand['yaku']['simple']['chinitsu'] = True
            if a_hand['is_open']:
                han -= 1
    else:
        if (((a_hand['honor_sets'] + a_hand['manzu_sets']) >= 5) or (
                (a_hand['honor_sets'] + a_hand['souzu_sets']) >= 5) or (
                (a_hand['honor_sets'] + a_hand['pinzu_sets']) >= 5) and a_hand[
            'honor_sets']):
            han = 3
            a_hand['yaku']['simple']['honitsu'] = True
            if a_hand['is_open']:
                han -= 1

        elif ((a_hand['manzu_sets'] == 5) or (a_hand['souzu_sets'] == 5) or (
                a_hand['pinzu_sets'] == 5)):
            han = 6
            a_hand['yaku']['simple']['chinitsu'] = True
            if a_hand['is_open']:
                han -= 1

    a_hand["base_han"] += han


def find_pinfu(a_hand: dict):
    if (not a_hand['additional_fu']) and (not a_hand['is_open']) and (a_hand['wait'] == 'ryanmen'):
        a_hand['yaku']['simple']['pinfu'] = True
        a_hand["base_han"] += 1


# methods to with non-flat yaku


def find_sananko(a_hand: dict):
    if ((a_hand['pon_amount'] + a_hand['kan_amount']) - (a_hand['opened_kans'] + a_hand['opened_pons'])) == 3:
        a_hand['yaku']['simple']['sananko'] = True
        a_hand["base_han"] += 2


def find_sandoko(a_hand: dict):
    if a_hand['identical_pons'] == 3:
        han = 2
        a_hand['yaku']['simple']['sandoko'] = True
        a_hand['base_han'] += han


def find_sesangen(a_hand: dict):
    if (a_hand['dragon_pons'] == 2) and (a_hand['dragon_pair']):
        han = 2
        a_hand['yaku']['simple']['sesangen'] = True
        a_hand['base_han'] += han


def find_sankatsu(a_hand: dict):
    if a_hand['kan_amount'] == 3:
        han = 2
        a_hand['yaku']['simple']['sankatsu'] = True
        a_hand['base_han'] += han


####-------------------------------------Yakuman finders-----------------------------------------------------
# yakuman_yaku_list = ['suanko', 'sukatsu', 'chonroto', 'daisangen',
#                      'sosushi', 'daishushi', 'tsuiso', 'kokushi musou',
#                      'churenpoto', 'ruisou']


def find_suanko(a_hand: dict):
    if ((a_hand['pon_amount'] + a_hand['kan_amount']) - (a_hand['opened_kans'] + a_hand['opened_pons'])) == 4:
        a_hand['yaku']['special']['suanko'] = True
        a_hand["base_han"] = 13


def find_sukatsu(a_hand: dict):
    if a_hand['kan_amount'] == 4:
        a_hand['yaku']['special']['sukatsu'] = True
        a_hand['base_han'] = 13


def find_chonroto(a_hand: dict):
    if ((a_hand["border_pons"] + a_hand["border_kans"]) > 3) and a_hand["border_pair"]:
        a_hand['yaku']['special']['chonroto'] = True
        a_hand['base_han'] = 13


def find_daisangen(a_hand: dict):
    if (a_hand['dragon_pons'] + a_hand['dragon_kans']) == 3:
        a_hand['yaku']['special']['daisangen'] = True
        a_hand['base_han'] = 13


def find_sosushi_daishushi(a_hand: dict):
    if (a_hand['wind_pons'] + a_hand['wind_kans']) > 3:
        a_hand['yaku']['special']['daisushi'] = True
        a_hand['base_han'] = 26
    elif ((a_hand['wind_pons'] + a_hand['wind_kans']) == 3) and a_hand['wind_pair']:
        a_hand['yaku']['special']['sosushi'] = True
        a_hand['base_han'] = 13


def find_tsuiso(a_hand: dict):
    if a_hand['is_chiitoi']:
        if a_hand['honor_sets'] == 7:
            a_hand['yaku']['special']['tsuiso'] = True
            a_hand['base_han'] = 13
    else:
        if a_hand['honor_sets'] == 5:
            a_hand['yaku']['special']['tsuiso'] = True
            a_hand['base_han'] = 13


def find_kokushi_musou(a_hand: dict):
    pass


def find_churenpoto(a_hand: dict):
    if (not a_hand['is_open']) and (not a_hand['kan_amount']):
        hand = a_hand['hand'].copy()
        hand_c = "".join(sorted("".join([i[0] for i in hand]).replace('-', '')))
        if a_hand['manzu_sets'] > 4:

            if hand_c in churenpoto_samples['manzu']:
                a_hand['yaku']['special']['churenpoto'] = True
                a_hand['base_han'] = 13


        elif a_hand['souzu_sets'] > 4:

            if hand_c in churenpoto_samples['souzu']:
                a_hand['yaku']['special']['churenpoto'] = True
                a_hand['base_han'] = 13


        elif a_hand['pinzu_sets'] > 4:

            if hand_c in churenpoto_samples['pinzu']:
                a_hand['yaku']['special']['churenpoto'] = True
                a_hand['base_han'] = 13


def find_ruisou(a_hand: dict):
    ruisou_available_tiles = ["🀅", "🀑", "🀒", "🀓", "🀕", "🀗", '🀫', '-']
    flag = True
    ruisou_flag = True
    if ((a_hand['souzu_sets'] > 3) and (not a_hand['manzu_sets'] and not a_hand['pinzu_sets']) and
        not a_hand['border_chis'] and not a_hand['border_pair'] and not a_hand['border_pons'] and not
            a_hand['border_kans']) and not a_hand['wind_kans'] and not a_hand['wind_pons'] and not a_hand['wind_pair']:
        for i in a_hand['hand']:
            for j in i[0]:
                if j not in ruisou_available_tiles:
                    # print(a_hand['hand'])
                    # print('FALSE!!')
                    flag = False
                    ruisou_flag = False
                    break
            if not flag:
                break
        else:
            if ruisou_flag:
                a_hand['yaku']['special']['ruisou'] = True
                a_hand['base_han'] = 13
