



def main():
    from src.main_controller import Main_Controller
    
    main_object = Main_Controller()
    #main_object.update_realm_data()
    
    main_object.Postgress_DB.show_table("realms")
    
    
    
if __name__ == "__main__":
    main()