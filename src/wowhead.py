import requests
import xmltodict
import json

try:
    from src.Objects.Item_Attributes import Item, Rarity
    from src.Objects.itemClass       import get_item_class, get_subclass_name
except:
    from Objects.Item_Attributes import Item, Rarity
    from Objects.itemClass       import get_item_class, get_subclass_name

class Scraper:
    def __init__(self):
        self.base_MoP_URL = "https://www.wowhead.com/mop-classic/item="
        
    async def get_item_data(self, item_id:int):
        import regex
        
        response = requests.get(f"{self.base_MoP_URL}{item_id}&xml")
        if not response.status_code == 200:
            return None
        response_dict: dict = xmltodict.parse(response.content.decode("utf-8"))["wowhead"]["item"]
        if "createdBy" in response_dict.keys():
            pass
        
        name   = response_dict["name"]
        rarety = response_dict["quality"]["@id"]
        
        sell_price = regex.findall("sellprice\":([0-9]*)", response_dict.get("jsonEquip", ""))
        buy_price  = regex.findall("buyprice\":([0-9]*)" , response_dict.get("jsonEquip", ""))  
           
        vendor_sell_price = int(sell_price[0]) if len(sell_price) == 1 else None
        vendor_buy_price  = int(buy_price[0] ) if len(buy_price)  == 1 else None
        
        itemClass    = get_item_class(response_dict["class"]["@id"])
        itemSubClass = get_subclass_name(itemClass.id, response_dict["subclass"]["@id"])
        
        return Item(
            id        = item_id,
            ItemClass = itemClass.name,
            itemSubClass    = itemSubClass,
            name            = name,
            rarety          = rarety,
            vendor_sell_price   = vendor_sell_price,
            vendor_buy_price    = vendor_buy_price    
        ) 
        

if __name__ == "__main__":
    import asyncio
    s = Scraper()
    i = asyncio.run(s.get_item_data(72234))
    print(i.itemSubClass)