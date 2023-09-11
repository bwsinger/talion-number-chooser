from dataclasses import dataclass, field


@dataclass
class MTGCard:
    id: str
    name: str
    cmc: float
    power: str = ''
    toughness: str = ''
    quantity: int = 1
