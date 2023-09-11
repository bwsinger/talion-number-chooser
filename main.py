import os
from src.fetch import get_all_moxfield_decklist_cards
from src.settings import DECKLIST_PATH
from src.core import get_decklist_ids

if __name__ == "__main__":
    deck_ids = []

    if os.path.isfile(DECKLIST_PATH):
        with open(DECKLIST_PATH, "r", encoding="utf-8") as f:
            # Extract the decklist IDs from the URLs
            deck_ids = get_decklist_ids(f.readlines())


    cards = get_all_moxfield_decklist_cards(deck_ids)

    results = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
    }

    for card in cards:
        attributes = set((card.cmc, card.power, card.toughness))

        for attr in attributes:
            if results.get(attr) is not None:
                results[attr] += card.quantity

    # Stats
    total_hits = sum([value for key,value in results.items()])

    print(f'Number     Count       Percentage')
    print('---------------------------------')

    for key, value in results.items():
        percentage = round((value/total_hits) * 100, 2)
        print(f'[{int(key):2d}]: {value:10d} {percentage:11.2f}')
