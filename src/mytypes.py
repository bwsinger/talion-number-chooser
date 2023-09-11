from dataclasses import dataclass
from typing import Optional


@dataclass
class MTGCard:
    id: str
    name: str
    cmc: str
    power: Optional[str] = None
    toughness: Optional[str] = None
    quantity: int = 1
