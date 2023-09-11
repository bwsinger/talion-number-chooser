import json
import re
from typing import Callable, Optional, Any

import requests
from backoff import on_exception, expo
from ratelimit import RateLimitDecorator, sleep_and_retry
from requests import RequestException

from .types import MTGCard


moxfield_rate_limit = RateLimitDecorator(calls=20, period=1)


"""
DECORATORS
"""


def handle_final_exception(fail_response: Optional[Any]) -> Callable:
    """
    Decorator to handle any exception and return appropriate failure value.
    @param fail_response: Return value if Exception occurs.
    @return: Return value of the function, or fail_response.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Final exception catch
            try:
                return func(*args, **kwargs)
            except (RequestException, json.JSONDecodeError):
                # All requests failed
                return fail_response

        return wrapper

    return decorator


def handle_moxfield_request(fail_response: Optional[Any] = None) -> Callable:
    """
    Decorator to handle all Moxfield request failure cases, and return appropriate failure value.
    @param fail_response: The value to return if request failed entirely.
    @return: Requested data if successful, fail_response if not.
    """

    def decorator(func):
        @sleep_and_retry
        @moxfield_rate_limit
        @on_exception(expo, RequestException, max_tries=2, max_time=0.75)
        @handle_final_exception(fail_response)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


"""
MOXFIELD REQUESTS
"""

@handle_moxfield_request({})
def get_data_url(url: str, params: Optional[dict[str, str]] = None) -> dict:
    """
    Get JSON data from any valid API URL.
    @param url: Valid API URL, such as Moxfield.
    @param params: Params to pass to an API endpoint.
    @return: JSON data returned.
    """
    with requests.get(url, params=(params or {})) as response:
        if response.status_code == 200:
            return response.json() or {}
        return {}


"""
UTILITY FUNCTIONS
"""


def get_cards_from_moxfield_decklist(url: str, params: Optional[dict[str, str]] = None) -> list[MTGCard]:
    """
    Extract the card info from a single Moxfield decklist.
    @param url: Either the API endpoint or full URL.
    @param params: Optional parameters to pass to API endpoint.
    """
    cards: list[MTGCard] = list()

    res_json = get_data_url(url) or {}

    main_raw = res_json.get('mainboard', None)
    commander_raw = res_json.get('commanders', None)

    # If the mainboard is empty, skip this decklist as something went wrong
    if not isinstance(main_raw, dict):
        return []

    raw_cards = {**main_raw, **commander_raw}

    for raw_card in raw_cards:
        card = MTGCard()
        card.id = raw_card.get('card', {}).get('id')
        card.name = raw_card.get('card', {}).get('name')
        card.name = raw_card.get('card', {}).get('cmc')
        card.power = raw_card.get('card', {}).get('power', '')
        card.toughness = raw_card.get('card', {}).get('toughness', '')
        card.quantity = raw_card.get('quantity', 1)

    return cards


def get_all_moxfield_decklist_cards(params: dict) -> list[MTGCard]:
    """
    Lookup Card data for every decklist in the config on Moxfield.
    @note: https://api.moxfield.com/v2/decks/all/{deck_id}
    @param params: Likley not needed, but leaving the option open.
    @return: Card data as dict.
    """
    # TODO: Get decklists from config file
    decklists = ['https://api.moxfield.com/v2/decks/all/hHcoQkbo2kWxXSCNyXGX5A']

    all_cards: list[MTGCard] = list()

    for decklist in decklists:
        # Extract the deck_id from a valid Moxfield decklist URL
        deck_id_match = re.search(r'moxfield\.com\/decks\/(.{22})$', decklist)

        if deck_id_match is None:
            continue

        deck_id = deck_id_match.group(1)

        cards = get_cards_from_moxfield_decklist(f"https://api.moxfield.com/v2/decks/all/{deck_id}", params=params)

        all_cards.extend(cards)
    
    return all_cards or []