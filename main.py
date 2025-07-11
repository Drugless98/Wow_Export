from src.main_controller import Main_Controller

#: Gehennas Europe MoP = region: 14, AH_horde = 392
def show_regions(mc: Main_Controller)    : mc.Postgress_DB.show_table("regions")
def show_region_data(mc: Main_Controller): mc.Postgress_DB.show_all_region_data(14) 



def main():
    
    
    main_object = Main_Controller()
    main_object.set_AH_id(392)

    import json
    print(json.dumps(main_object.get_AH_item(52722)))
    
    
    
if __name__ == "__main__":
    main()