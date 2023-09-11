from src.fetch import get_all_moxfield_decklist_cards

if __name__ == "__main__":
    # TODO: Get decklists from config file
    decklists = [
        'https://www.moxfield.com/decks/hHcoQkbo2kWxXSCNyXGX5A',
        'https://www.moxfield.com/decks/1ywQ_gE8jUuPBosTXFyZSQ',
        'https://www.moxfield.com/decks/TO9kxf5Gl0OpmOHQ0p5ugQ',
        'https://www.moxfield.com/decks/ujKCddgPHEq3BJv86FjUYg',
    ]

    cards = get_all_moxfield_decklist_cards(decklists)

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

    for key, value in results.items():
        print(f'[{key:2s}]: {value}')
