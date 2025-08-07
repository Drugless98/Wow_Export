from src.main_controller import Main_Controller
from src.GoogleSync import GSheet_Controller

import pandas as pd


#: Gehennas Europe MoP = region: 14, AH_horde = 392
def show_regions(mc: Main_Controller)    : mc.Postgress_DB.show_table("regions")
def show_region_data(mc: Main_Controller): mc.Postgress_DB.show_all_region_data(14) 



def main():
   
    main_object = Main_Controller()
    GSheet = GSheet_Controller()
    main_object.set_AH_id(392)

    items_missing_in_itemsTable = main_object.Postgress_DB.get_missing_item_data()
    main_object.DB_add_items(items_missing_in_itemsTable)
    
    main_object.update_item_data_ASYNC()
    main_object.update_item_price_hist_ASYNC()
    
    from datetime import datetime
    headers = [f"Updated: {datetime.now().strftime("%H:%M")}","name","vendor_sell_price","vendor_buy_price","marketvalue","quantity","avg_sale_price","sale_rate","sold_perday","min_buyout"]
    data = main_object.Postgress_DB.get_table_data("SELECT * FROM excel_export")
    pandas_data_dict = {}
    
    for row in data:
        for idx, col in enumerate(headers):
            if not col in pandas_data_dict:
                pandas_data_dict[col] = [row[idx]]
            else:
                pandas_data_dict[col].append(row[idx])
    
    df = pd.DataFrame(pandas_data_dict)
    GSheet.write_pd_toSheet(df)
    
    items_ids = main_object.Postgress_DB.get_query("SELECT item_id FROM item_prices ip LEFT JOIN items i ON ip.item_id = i.id WHERE i.id IS NULL")
    main_object.DB_add_items(items_ids)
    
    
    
if __name__ == "__main__":
    from datetime import datetime
    import time

    main()    
    TIMEINTERVAL = 900 #: 15 min
    while True:
        if datetime.now().minute % 15 == 0: #At min 00, 15, 30 and 45
            print("Started to update")
            main()
            print(f"Done updating at: {datetime.now()}")
        time.sleep(60)    
        
    
