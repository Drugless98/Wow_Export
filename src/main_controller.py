
from src.Database   import Postgress
from src.TSM        import API
from src            import Local    

from src.Objects.Item_Attributes import Item, Rarity
from src.ASync_task_manager      import Async_Postgress


class Main_Controller:
    def __init__(self, set_defaults=True):
        self.Postgress_DB    = Postgress()
        self.async_postgress = Async_Postgress()
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

    def add_item_price_data(self):
        item_data = self.get_all_items_regions()
        items_count = len(item_data)
        item_counter= 0

        for item in item_data:
            self.Postgress_DB.add_item_price_data(
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
            
    def update_item_data_ASYNC(self):
        import asyncio
        from src.Objects.Item_Attributes import Item_prices

    #: Start the Async loop
        async def run_async(item_data: list[Item_prices], region_data_exists: bool):
            await self.async_postgress.connect()

            tasks = []
            total = len(item_data)

            for idx, item in enumerate(item_data, start=1):
                if region_data_exists:
                    task = self.async_postgress.add_item_price_data(
                        id=item.id,
                        minBuyout=item.min_buyout,
                        market_value=item.marketvalue,
                        quantity=item.quantity,
                        avg_sale_price=item.avg_sale_price,
                        sale_rate=item.sale_rate,
                        sold_perday=item.sold_perday
                    )
                else:
                    task = self.async_postgress.update_minbuyout_quantity_only(
                        id=item.id,
                        minBuyout=item.min_buyout,
                        quantity=item.quantity
                    )

                async def wrapped_task(t=task, i=idx, n=total):
                    await t
                    print(f"{i} / {n}")
                tasks.append(wrapped_task())

            await asyncio.gather(*tasks)
            await self.async_postgress.Connection_Pool.close()
            
    #: Data preperations 
        item_region_data = self.get_all_items_regions()
        item_ah_data = self.get_all_items_ah()

        region_exists = item_region_data is not None

        #: Regions restrict only 10 calls per day, so if restriction met.
        if not region_exists:
            update_data = [Item_prices(
                id=item_key,
                min_buyout=item_ah_data[item_key]["minBuyout"],
                quantity=item_ah_data[item_key]["quantity"],
                marketvalue=None,
                avg_sale_price=None,
                sale_rate=None,
                sold_perday=None
            ) for item_key in item_ah_data.keys()]
        else:
            update_data = [Item_prices(
                id=item_key,
                min_buyout=item_ah_data[item_key]["minBuyout"],
                quantity=item_ah_data[item_key]["quantity"],
                marketvalue=item_region_data[item_key]["marketValue"],
                avg_sale_price=item_region_data[item_key]["avgSalePrice"],
                sale_rate=item_region_data[item_key]["saleRate"],
                sold_perday=item_region_data[item_key]["sold_perday"]
            ) for item_key in item_ah_data.keys() if item_key in item_region_data]
            
        self.Update_data = update_data
        asyncio.run(run_async(update_data, region_exists))
        
    def DB_add_items(self, items_to_add: list[int]):
        import asyncio
        from src.wowhead import Scraper
        scraper = Scraper()
        
        if len(items_to_add) == 0:
            return 
        
        async def run_async(items: list[Item]):
            await self.async_postgress.connect()

            tasks = []
            total = len(items)
            for idx, item_id in enumerate(items, start=1):
                item_obj = await scraper.get_item_data(item_id)
                if item_obj is None:
                    print(f"Skipped item {item_id} — no data")
                    continue

                task_t = self.async_postgress.add_item_data(item_obj)

                async def wrapped_task(task=task_t, i=idx, n=total):
                    print(f"Started {i}/{n}")
                    await task
                    print(f"Inserted {i}/{n}")

                tasks.append(wrapped_task())
                
            #: Gather and run all inserts
            await asyncio.gather(*tasks)
            await self.async_postgress.Connection_Pool.close()
        asyncio.run(run_async(items_to_add))

    def update_item_price_hist_ASYNC(self):
        import asyncio
        from src.Objects.Item_Attributes import Item_prices

    #: Start the Async loop
        async def run_async(item_data: list[Item_prices]):
            await self.async_postgress.connect()

            tasks = []
            total = len(item_data)

            for idx, item in enumerate(item_data, start=1):
                task = self.async_postgress.add_item_price_hist(item)
                async def wrapped_task(t=task, i=idx, n=total):
                    await t
                    print(f"{i} / {n}")
                tasks.append(wrapped_task())

            await asyncio.gather(*tasks)
            await self.async_postgress.Connection_Pool.close()
        asyncio.run(run_async(self.Update_data))
        
        


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