from src.main_controller import Main_Controller

#: Gehennas Europe MoP = region: 14, AH_horde = 392
def show_regions(mc: Main_Controller)    : mc.Postgress_DB.show_table("regions")
def show_region_data(mc: Main_Controller): mc.Postgress_DB.show_all_region_data(14) 



def main():
    
    
    main_object = Main_Controller()
    main_object.set_AH_id(392)

    import json


    #main_object.write_json(json.dumps(main_object.get_all_items_regions(14), indent=2))
    main_object.update_item_data()
    
    
    
if __name__ == "__main__":
    main()