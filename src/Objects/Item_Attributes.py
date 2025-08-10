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
    ItemClass         : str 
    itemSubClass      : str       
    name              : str       
    rarety            : Rarity    
    vendor_sell_price : int       
    vendor_buy_price  : int       
    
@dataclass
class Item_prices:
    id              : int
    marketvalue     : int
    min_buyout      : int
    quantity        : int
    avg_sale_price  : int
    sale_rate       : float
    sold_perday     : float