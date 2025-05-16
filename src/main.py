import time
from pprint import pprint

from src.calculations import CalculatedHand
from src.hand import Hand
from src.wall import Wall
from src.yaku_list import simple_yaku_list, hard_yaku_list, yakuman_yaku_list


def check_all_simple_yaku():
    start = time.time()
    while len(simple_yaku_list):
        wall = Wall()
        hand = Hand(wall)
        calculated_hand = CalculatedHand(hand)
        result_hand = calculated_hand.get_result_hand()
        if result_hand['is_valid']:
            collected_yaku = []
            for yaku in result_hand['yaku']['simple'].keys():
                if yaku in simple_yaku_list:
                    collected_yaku.append(yaku)
            if collected_yaku:
                print('-' * 100)
                for col_yaku in collected_yaku:
                    simple_yaku_list.pop(simple_yaku_list.index(col_yaku))
                pprint(result_hand)
                print(f'Collected essential yaku in this hand: '
                      f'{collected_yaku}')
                print(f'Remaining yaku: {simple_yaku_list}')
                print('-' * 100)
                print()
    end = time.time()
    print(f'Time spent on collectin all essential yaku: {(end - start):.3f} seconds.')


def check_all_hard_yaku():
    start = time.time()
    while len(hard_yaku_list):
        wall = Wall()
        hand = Hand(wall)
        calculated_hand = CalculatedHand(hand)
        result_hand = calculated_hand.get_result_hand()
        if result_hand['is_valid']:
            collected_yaku = []
            for yaku in result_hand['yaku']['simple'].keys():
                if yaku in hard_yaku_list:
                    collected_yaku.append(yaku)
            if collected_yaku:
                print('-' * 100)
                for col_yaku in collected_yaku:
                    hard_yaku_list.pop(hard_yaku_list.index(col_yaku))
                pprint(result_hand)
                print(f'Collected hard yaku in this hand: '
                      f'{collected_yaku}')
                print(f'Remaining yaku: {hard_yaku_list}')
                print(calculated_hand.wall_data.ALL_TILES[result_hand['suit_win_tile']])
                print(calculated_hand.wall_data.ALL_TILES[result_hand['suit_win_tile']].get(result_hand['win_tile']))
                print(calculated_hand.wall_data.DEAD_WALL)
                print('-' * 100)
    end = time.time()
    print(f'Time spent on collectin all hard yaku: {(end - start):.3f} seconds.')


def check_all_yakumans():
    start = time.time()
    while len(yakuman_yaku_list):
        wall = Wall()
        hand = Hand(wall)
        calculated_hand = CalculatedHand(hand)
        result_hand = calculated_hand.get_result_hand()
        if result_hand['is_valid']:
            collected_yaku = []
            for yaku in result_hand['yaku']['special'].keys():
                if yaku in yakuman_yaku_list:
                    collected_yaku.append(yaku)
            if collected_yaku:
                print('-' * 100)
                for col_yaku in collected_yaku:
                    yakuman_yaku_list.pop(yakuman_yaku_list.index(col_yaku))
                pprint(result_hand)
                print(f'Collected yakumans in this hand: '
                      f'{collected_yaku}')
                print(f'Remaining yakumans: {yakuman_yaku_list}')
                print(calculated_hand.wall_data.ALL_TILES[result_hand['suit_win_tile']])
                print(calculated_hand.wall_data.ALL_TILES[result_hand['suit_win_tile']].get(result_hand['win_tile']))
                print(calculated_hand.wall_data.DEAD_WALL)
                print('-' * 100)
    end = time.time()
    print(f'Time spent on collectin all yakumans: {(end - start):.3f} seconds.')


def pretty_wall_show(count_hands=1):
    while count_hands:
        wall = Wall()
        hand = Hand(wall)
        calculated_hand = CalculatedHand(hand)
        result_hand = calculated_hand.get_result_hand()
        if result_hand['is_valid']:
            print(calculated_hand.a_hand.get_simple_hand())
            count_hands -= 1


if __name__ == '__main__':
    # check_all_simple_yaku()
    # check_all_hard_yaku()
    # check_all_yakumans()

    pretty_wall_show(10)
