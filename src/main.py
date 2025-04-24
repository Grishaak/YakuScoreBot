from pprint import pprint
from time import sleep

from src.hand import Hand
from src.wall import Wall

if __name__ == '__main__':
    for i in range(1):
        for k in enumerate(('ad','dasd')):
            print(k)
        wall = Wall()
        hand = Hand(wall)
        hand.yaku_calculator()
        pprint(hand.get_data_hand(), indent=2, width=120)
        hand.build_dead_wall()
        print('-'*100)
        sleep(4)
