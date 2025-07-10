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
        headers = {"Authorization": f"Bearer {self.Access_Token}"}
        response = requests.get("https://realm-api.tradeskillmaster.com/realms", headers=headers)
        load_response = json.loads(response.content)
        
        return json.dumps(load_response, indent=2) if response.status_code < 400 else None


if __name__ == "__main__":
    api = API()
    realms_response = api.get_realms()
    print(json.dumps(realms_response, indent=2))