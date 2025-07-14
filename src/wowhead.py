import requests
import xmltodict
import json

try:
    from src.Objects.Item_Attributes import Item, Rarity
except:
    from Objects.Item_Attributes import Item, Rarity

class Scraper:
    def __init__(self):
        self.base_MoP_URL = "https://www.wowhead.com/mop-classic/item="
        
    async def get_item_data(self, item_id:int):
        import regex
        
        response = requests.get(f"{self.base_MoP_URL}{item_id}&xml")
        if not response.status_code == 200:
            return None
        
        item = Item(item_id)
        response_dict: dict = xmltodict.parse(response.content.decode("utf-8"))["wowhead"]["item"]
        if "createdBy" in response_dict.keys():
            pass
        
        item.name   = response_dict["name"]
        item.rarety = response_dict["quality"]["@id"]
        
        sell_price = regex.findall("sellprice\":([0-9]*)", response_dict.get("jsonEquip", ""))
        buy_price  = regex.findall("buyprice\":([0-9]*)" , response_dict.get("jsonEquip", ""))
        
        item.vendor_sell_price = int(sell_price[0]) if len(sell_price) == 1 else None
        item.vendor_buy_price  = int(buy_price[0] )   if len(buy_price)  == 1 else None
        
        return item 
        

if __name__ == "__main__":
    s = Scraper()
    s.get_item_data(71249)