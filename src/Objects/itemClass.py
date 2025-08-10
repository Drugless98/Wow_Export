from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(frozen=True)
class Subclass:
    id: int
    name: str


@dataclass(frozen=True)
class ItemClassData:
    id: int
    name: str
    subclasses: Tuple[Subclass, ...] = ()


ITEM_CLASSES: Tuple[ItemClassData, ...] = (
    ItemClassData(
        0, "Consumable",
        (
            Subclass(0, "Consumable"),
            Subclass(1, "Potion"),
            Subclass(2, "Elixir"),
            Subclass(3, "Flask"),
            Subclass(4, "Scroll"),
            Subclass(5, "Food & Drink"),
            Subclass(6, "Item Enhancement"),
            Subclass(7, "Bandage"),
            Subclass(8, "Other"),
            Subclass(9, "Vantus Rune"),
        ),
    ),
    ItemClassData(1, "Container", ()),
    ItemClassData(
        2, "Weapon",
        (
            Subclass(0, "One-Handed Axe"),
            Subclass(1, "Two-Handed Axe"),
            Subclass(2, "Bow"),
            Subclass(3, "Gun"),
            Subclass(4, "One-Handed Mace"),
            Subclass(5, "Two-Handed Mace"),
            Subclass(6, "Polearm"),
            Subclass(7, "One-Handed Sword"),
            Subclass(8, "Two-Handed Sword"),
            Subclass(9, "Warglaive"),
            Subclass(10, "Staff"),
            Subclass(11, "Bear Claw"),
            Subclass(12, "Cat Claw"),
            Subclass(13, "Fist Weapon"),
            Subclass(14, "Miscellaneous"),
            Subclass(15, "Dagger"),
            Subclass(16, "Thrown"),
            Subclass(17, "Spear"),
            Subclass(18, "Crossbow"),
            Subclass(19, "Wand"),
            Subclass(20, "Fishing Pole"),
        ),
    ),
    ItemClassData(3, "Gem", ()),
    ItemClassData(
        4, "Armor",
        (
            Subclass(0, "Miscellaneous"),
            Subclass(1, "Cloth"),
            Subclass(2, "Leather"),
            Subclass(3, "Mail"),
            Subclass(4, "Plate"),
            Subclass(5, "Cosmetic"),
            Subclass(6, "Shield"),
            Subclass(7, "Libram"),
            Subclass(8, "Idol"),
            Subclass(9, "Totem"),
            Subclass(10, "Sigil"),
            Subclass(11, "Relic"),
        ),
    ),
    ItemClassData(5, "Reagent (Obsolete)", ()),
    ItemClassData(6, "Projectile (Obsolete)", ()),
    ItemClassData(
        7, "Tradeskill",
        (
            Subclass(0, "Trade Goods"),
            Subclass(1, "Parts"),
            Subclass(2, "Explosives"),
            Subclass(3, "Devices"),
            Subclass(4, "Jewelcrafting"),
            Subclass(5, "Cloth"),
            Subclass(6, "Leather"),
            Subclass(7, "Metal & Stone"),
            Subclass(8, "Meat"),
            Subclass(9, "Herb"),
            Subclass(10, "Elemental"),
            Subclass(11, "Other"),
            Subclass(12, "Enchanting"),
            Subclass(13, "Material"),
            Subclass(14, "Item Enchantment"),
            Subclass(15, "Weapon Enchantment"),
            Subclass(16, "Inscription"),
        ),
    ),
    ItemClassData(8, "Item Enhancement", ()),
    ItemClassData(
        9, "Recipe",
        (
            Subclass(0, "Book"),
            Subclass(1, "Leatherworking"),
            Subclass(2, "Tailoring"),
            Subclass(3, "Engineering"),
            Subclass(4, "Blacksmithing"),
            Subclass(5, "Cooking"),
            Subclass(6, "Alchemy"),
            Subclass(7, "First Aid"),
            Subclass(8, "Enchanting"),
            Subclass(9, "Fishing"),
            Subclass(10, "Jewelcrafting"),
            Subclass(11, "Inscription"),
        ),
    ),
    ItemClassData(10, "Money (Obsolete)", ()),
    ItemClassData(11, "Quiver (Obsolete)", ()),
    ItemClassData(12, "Quest", ()),
    ItemClassData(13, "Key", ()),
    ItemClassData(14, "Permanent (Obsolete)", ()),
    ItemClassData(
        15, "Miscellaneous",
        (
            Subclass(0, "Junk"),
            Subclass(1, "Reagent"),
            Subclass(2, "Companion Pet"),
            Subclass(3, "Holiday"),
            Subclass(4, "Other"),
            Subclass(5, "Mount"),
        ),
    ),
    ItemClassData(16, "Glyph", ()),
    ItemClassData(17, "Battle Pets", ()),
    ItemClassData(18, "WoW Token", ()),
    ItemClassData(19, "Profession", ()),
)


def get_item_class(class_id: int) -> Optional[ItemClassData]:
    return next((cls for cls in ITEM_CLASSES if cls.id == int(class_id)), None)


def get_subclass_name(class_id: int, subclass_id: int) -> Optional[str]:
    cls = get_item_class(class_id)
    if not cls:
        return None
    sub = next((sc for sc in cls.subclasses if sc.id == int(subclass_id)), None)
    return sub.name if sub else None

