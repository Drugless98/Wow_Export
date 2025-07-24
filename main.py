from src.main_controller import Main_Controller

#: Gehennas Europe MoP = region: 14, AH_horde = 392
def show_regions(mc: Main_Controller)    : mc.Postgress_DB.show_table("regions")
def show_region_data(mc: Main_Controller): mc.Postgress_DB.show_all_region_data(14) 



def main():
   
    main_object = Main_Controller()
    main_object.set_AH_id(392)

    import json

    #main_object.Postgress_DB.run_query("DROP TABLE item_prices")
    #main_object.Postgress_DB.run_local_sql()
    #main_object.update_item_data_ASYNC()
    #main_object.Postgress_DB.run_local_sql()
    
    #main_object.Postgress_DB.show_table("excel_export")

    #main_object.update_item_data_ASYNC()
    #main_object.update_item_price_hist_ASYNC()
        
    #items_ids = main_object.Postgress_DB.get_query("SELECT item_id FROM item_prices ip LEFT JOIN items i ON ip.item_id = i.id WHERE i.id IS NULL")
    #main_object.DB_add_items(items_ids)
    
    main_object.Postgress_DB.to_csv("price_history")
    
    
    
if __name__ == "__main__":
    from datetime import datetime
    import time
    
    TIMEINTERVAL = 900 #: 15 min
    
    main()
        
    