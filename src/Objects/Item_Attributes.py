from dataclasses import dataclass, field
from enum        import Enum   


class Rarity(Enum):
    COMMON    = 1
    UNCOMMON  = 2
    RARE      = 3
    EPIC      = 4
    LEGENDARY = 5

@dataclass
class Item:
    id                : int
    name              : str    = field(default=None)
    rarety            : Rarity = field(default=None)
    vendor_sell_price : int    = field(default=None)
    vendor_buy_price  : int    = field(default=None)
    
@dataclass
class Item_prices:
    id              : int
    marketvalue     : int
    min_buyout      : int
    quantity        : int
    avg_sale_price  : int
    sale_rate       : float
    sold_perday     : float