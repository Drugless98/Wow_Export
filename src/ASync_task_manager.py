import os
import asyncpg

try:    #: from main.py
    from src.Objects.Item_Attributes import Item, Item_prices
except: #: from self
    from Objects.Item_Attributes import Item, Item_prices
     
class Async_Postgress:
    def __init__(self):
        self.Connection_Pool = None
    
    async def connect(self):
        self.Connection_Pool = await asyncpg.create_pool(
            host        = os.getenv("HOST"),
            port        = 5432,
            database    = "wowdata",
            user        = os.getenv("DB_USER"),
            password    = os.getenv("DB_PASS"),
            min_size    = 1,
            max_size    = 50
        )
        
    async def add_item_price_hist(self, item: Item_prices):
        from datetime import datetime
        async with self.Connection_Pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO
                    price_history (item_id, item_price, time) 
                VALUES
                    ($1, $2, $3)
                ON CONFLICT
                    (id) DO UPDATE
                SET
                    item_price    = EXCLUDED.item_price,
                    time          = EXCLUDED.time  
            """, item.id, item.min_buyout, datetime.now())
        
    async def add_item_data(self, item:Item):
        async with self.Connection_Pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO
                    items (id, name, rarety, vendor_sell_price, vendor_buy_price, class, subclass) 
                VALUES
                    ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT
                    (id) DO UPDATE
                SET
                    name    = EXCLUDED.name,
                    rarety  = EXCLUDED.rarety,
                    vendor_sell_price   = EXCLUDED.vendor_sell_price,
                    vendor_buy_price    = EXCLUDED.vendor_buy_price,
                    class               = EXCLUDED.class,
                    subclass            = EXCLUDED.subclass
            """, item.id, item.name, int(item.rarety), item.vendor_sell_price, item.vendor_buy_price, item.ItemClass, item.itemSubClass)
        
    async def add_item_price_data(self, id, market_value, minBuyout, quantity, avg_sale_price, sale_rate, sold_perday):
        sale_rate = float(sale_rate) if sale_rate is not None else 0.0
        sold_perday = float(sold_perday) if sold_perday is not None else 0.0

        async with self.Connection_Pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO
                    item_prices (item_id, marketvalue, min_buyout, quantity, avg_sale_price, sale_rate, sold_perday)
                VALUES
                    ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT
                    (item_id) DO UPDATE
                SET
                    marketvalue    = EXCLUDED.marketvalue,
                    min_buyout     = EXCLUDED.min_buyout,
                    quantity       = EXCLUDED.quantity,
                    avg_sale_price = EXCLUDED.avg_sale_price,
                    sale_rate      = EXCLUDED.sale_rate,
                    sold_perday    = EXCLUDED.sold_perday
            """, id, market_value, minBuyout, quantity, avg_sale_price, sale_rate, sold_perday)
    
    async def update_minbuyout_quantity_only(self, id, minBuyout, quantity):
        async with self.Connection_Pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO item_prices (item_id, min_buyout, quantity)
                VALUES ($1, $2, $3)
                ON CONFLICT (item_id) DO UPDATE
                SET
                    min_buyout = EXCLUDED.min_buyout,
                    quantity   = EXCLUDED.quantity
            """, id, minBuyout, quantity)
