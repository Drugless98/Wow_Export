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
        FILE_TO_RUN = "Create_auctionhouses.sql"
        PATH = os.path.join(os.path.dirname(__file__), "Queries", "Table_Creations", FILE_TO_RUN)
        
        
        with open(PATH, "r") as sql_file:
            self.cur.execute(sql_file.read())
            self.cur.connection.commit()
        
    def run_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
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