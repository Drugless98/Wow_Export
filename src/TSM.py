import os  
import requests
import json


class API:
    def __init__(self):
        #: Load local enviroment
        from dotenv import load_dotenv
        load_dotenv()
        
        #: Make Acces token
        self.Access_Token = self.get_acces_token()    
        self.headers = {"Authorization": f"Bearer {self.Access_Token}"}
        self.Price_base_path = "https://pricing-api.tradeskillmaster.com/ah"
        self.AuctionHouse_id = None
    
    #: SETTERS
    def set_AH(self, auction_id): self.AuctionHouse_id = auction_id

    #: GETTERS
 
    #: FUNCTIONS    
    def get_acces_token(self):        
        BODY = {
        "client_id": "c260f00d-1071-409a-992f-dda2e5498536",
        "grant_type": "api_token",
        "scope": "app:realm-api app:pricing-api",
        "token": f"{os.getenv('TOKEN')}"    
        }
        
        response = requests.post("https://auth.tradeskillmaster.com/oauth2/token",json=BODY )
        loaded_content = json.loads(response.content)
        return loaded_content["access_token"]

    def get_realms(self):
        
        response = requests.get("https://realm-api.tradeskillmaster.com/realms", headers=self.headers)
        load_response = json.loads(response.content)
        
        return json.dumps(load_response, indent=2) if response.status_code < 400 else None
    
    def get_item(self, item_id):
        if not self.AuctionHouse_id:
            print("Set AH_id before checking prices, bonobo")
            return None
    
        print(self.AuctionHouse_id)
        response = requests.get(f"{self.Price_base_path}/{self.AuctionHouse_id}/item/{item_id}", headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return f"Error code: {response.status_code}"


if __name__ == "__main__":
    api = API()
    realms_response = api.get_realms()
    print(json.dumps(realms_response, indent=2))