
from src.Database   import Postgress
from src.TSM        import API
from src            import Local    


class Main_Controller:
    def __init__(self, set_defaults=True):
        self.Postgress_DB   = Postgress()
        self.Tsm_api        = API() 

        if set_defaults:
            self.set_AH_id(392)
            self.set_region_id(14)


    #: SETTERS
    def set_AH_id(self, ah_id): self.Tsm_api.set_AH(ah_id)
    def set_region_id(self, reg_id): self.Tsm_api.set_region(reg_id)

    #: GETTERS
    def get_AH_item(self, item_id)  : return self.Tsm_api.get_item(item_id)
    def get_all_items_ah(self)      : return self.Tsm_api.get_all_items_ah()
    def get_all_items_regions(self) : return self.Tsm_api.get_all_items_region()

    #: FUNCTIONS
    def write_json(self, data):
        Local.write_json(data)

    def update_item_data(self):
        item_data = self.get_all_items_regions()
        items_count = len(item_data)
        item_counter= 0

        for item in item_data:
            self.Postgress_DB.add_item_data(
                id              = item["itemId"],
                market_value    = item["marketValue"],
                petSpeciesId    = item["petSpeciesId"],
                quantity        = item["quantity"],
                avg_sale_price  = item["avgSalePrice"],
                sale_rate       = item["saleRate"],
                sold_perday     = item["soldPerDay"] 
            )
            item_counter += 1
            print(f"{item_counter}/{items_count}")



    def update_realm_data(self):
        from json import loads
        data = loads(self.Tsm_api.get_realms())
        counter = 0
        max_counter = len(data["items"])
        
        #: Add regions to DB
        for region in data["items"]:
            region_dict = region
            self.Postgress_DB.add_region(
                id      = region_dict["regionId"],
                name    = region_dict["name"],
                prefix  = region_dict["regionPrefix"],
                version = region_dict["gameVersion"]
            )
            
            #: Add each realm inside region to DB
            for realm in region_dict["realms"]:
                realm_dict = realm
                self.Postgress_DB.add_realm(
                    id          = realm_dict["realmId"],
                    region_id   = realm_dict["regionId"],
                    realm_name  = realm_dict["name"],
                    locale      = realm_dict["locale"]
                )

                #: Add each AH on that realm to DB
                for ah in realm_dict["auctionHouses"]:
                    ah_dict = ah
                    self.Postgress_DB.add_auction_house(
                        id      = ah_dict["auctionHouseId"],
                        realm_id= realm_dict["realmId"],
                        faction = ah_dict["type"]
                    )
            counter += 1
            print(f"Update: {counter}/{max_counter}")