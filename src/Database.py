import psycopg2
import os

from dotenv import load_dotenv
from psycopg2 import OperationalError



class Postgress:
    def __init__(self):
        load_dotenv()
        try:
            #Connect to DB
            self.conn = psycopg2.connect(
                host        = "37.187.252.56",
                port        = 5432,
                database    = "wowdata",
                user        = os.getenv("DB_USER"),
                password    = os.getenv("DB_PASS")
            )
            self.cur = self.conn.cursor()
        except OperationalError as e:
            print(e)
        
    def run_local_sql(self):
        #: Manuel input file, to dynamicly run seems unsafe
        FILE_TO_RUN = "Create_Item_prices.sql"
        PATH = os.path.join(os.path.dirname(__file__), "Queries", "Table_Creations", FILE_TO_RUN)
        
        with open(PATH, "r") as sql_file:
            self.cur.execute(sql_file.read())
            self.cur.connection.commit()
    
    def run_view_sql(self, name):
        PATH = os.path.join(os.path.dirname(__file__), "Queries", "View_Creations", name)
        
        with open(PATH, "r") as sql_file:
            self.cur.execute(sql_file.read())
            self.cur.connection.commit()
        
    def run_query(self, query):
        self.cur.execute(query)
        self.cur.connection.commit()
    
    def get_query(self, query):
        self.cur.execute(query)
        return [i[0] for i in self.cur.fetchall() if i[0]]
        
    def add_item(self, id, name, rarety, vendor_sell, vendor_buy):
        self.cur.execute("""
            INSERT INTO
                regions (id, name, rarety, vendor_sell_price, vendor_buy_price)
            VALUES 
                (%s, %s, %s, %s, %s)
            ON CONFLICT
                (id) DO UPDATE
            SET
                name        = EXCLUDED.name
                rarety      = EXCLUDED.rarety,
                vendor_sell_price = EXCLUDED.vendor_sell_price,
                vendor_buy_price = EXCLUDED.vendor_buy_price;
            """, (id, name, int(rarety), vendor_sell, vendor_buy))
        self.conn.commit()
        
    
    def add_item_price_data(self, id, market_value, petSpeciesId, quantity, avg_sale_price, sale_rate, sold_perday):
        try:
            sale_rate = float(sale_rate) if sale_rate is not None else 0.0
            sold_perday = float(sold_perday) if sold_perday is not None else 0.0

            self.cur.execute("""
                INSERT INTO
                    item_data (item_id, marketvalue, quantity, avg_sale_price, sale_rate, sold_perday)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
                ON CONFLICT
                    (item_id) DO UPDATE
                SET
                    marketvalue    = EXCLUDED.marketvalue,
                    quantity       = EXCLUDED.quantity,
                    avg_sale_price = EXCLUDED.avg_sale_price,
                    sale_rate      = EXCLUDED.sale_rate,
                    sold_perday    = EXCLUDED.sold_perday
            """, (id, market_value, quantity, avg_sale_price, sale_rate, sold_perday))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()  # Reset the connection so the next query can work
            print(f"❌ failed: {e}")
            print(id, market_value, petSpeciesId, quantity, avg_sale_price, sale_rate, sold_perday)

    
    def add_region(self, id, name, prefix, version):
        self.cur.execute("""
            INSERT INTO
                regions (id, region_name, prefix, game_version)
            VALUES 
                (%s, %s, %s, %s)
            ON CONFLICT
                (id) DO UPDATE
            SET
                region_name = EXCLUDED.region_name,
                prefix = EXCLUDED.prefix,
                game_version = EXCLUDED.game_version;
            """, (id, name, prefix, version))
        self.conn.commit()
        
    def add_realm(self, id, region_id, realm_name, locale):
        self.cur.execute("""
            INSERT INTO 
                realms (id, region_id, realm_name, locale)
            VALUES 
                (%s, %s, %s, %s)
            ON CONFLICT
                (id) DO UPDATE
            SET
                region_id = EXCLUDED.region_id,
                realm_name = EXCLUDED.realm_name,
                locale = EXCLUDED.locale;
            """, (id, region_id, realm_name, locale))
        self.conn.commit()

    
    def add_auction_house(self, id, realm_id, faction):
        self.cur.execute("""
            INSERT INTO 
                auctionhouses (id, realm_id, faction)
            VALUES 
                (%s, %s, %s)
            ON CONFLICT 
                (id) DO UPDATE
            SET
                realm_id = EXCLUDED.realm_id,
                faction = EXCLUDED.faction;
            """, (id, realm_id, faction))
        self.conn.commit()
        
    def show_all_region_data(self, region_id):
        from tabulate import tabulate
        self.cur.execute("""
            SELECT 
                regions.region_name,
                regions.game_version,
                realms.realm_name,
                realms.locale,
                auctionhouses.faction,
                auctionhouses.id   
            FROM 
                regions
            JOIN
                realms ON regions.id = realms.region_id 
            JOIN
                auctionhouses ON realms.id = auctionhouses.realm_id
            WHERE
                regions.id = %s;      
            """, (region_id,))
        rows = self.cur.fetchall()
        headers = [desc[0] for desc in self.cur.description]
        print(tabulate(rows, headers=headers, tablefmt="pretty"))
        
        
    def show_table(self, table_name):
        from tabulate import tabulate
        self.cur.execute(f"SELECT * FROM {table_name};")
        rows = self.cur.fetchall()
        headers = [desc[0] for desc in self.cur.description]
        print(tabulate(rows, headers=headers, tablefmt="pretty"))

if __name__ == "__main__":
    p = Postgress()
    p.run_query("ALTER TABLE item_data ALTER COLUMN avg_sale_price TYPE BIGINT;")