from typing import List
import os
import re

cwd = os.getcwd()


"""
PRE-PROCESS DATA
"""


def get_decklist_ids(decklist_urls: List[str]) -> List[str]:
    """
    Normalizes a list of Moxfield decklist IDs from URLs, correcting for inconsistencies.
    @param decklist_urls: List of Moxfield URLs.
    @return: Normalized list of Moxfield decklist IDs.
    """

    deck_ids: List[str] = []

    # Remove empty lines
    for url in decklist_urls:
        if re.search(r'^\s*$', url):
            decklist_urls.remove(url)

    # Extract the deck_id from a valid Moxfield decklist URL
    for url in decklist_urls:
        deck_id_match = re.search(r'moxfield\.com\/decks\/(.{22})$', url)

        if deck_id_match is None:
            continue

        deck_ids.append(deck_id_match.group(1))

    return deck_ids