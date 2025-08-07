from gspread_pandas import Spread
import pandas as pd


class GSheet_Controller:
    def __init__(self) -> None:
        pass

    def write_pd_toSheet(self, df: pd.DataFrame):
        import os
        from oauth2client.service_account import ServiceAccountCredentials

        # Define the scopes
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # Load credentials from key.json file
        key_path = os.path.join(os.path.dirname(__file__), "key.json")
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)

        
        # Path to service account key file
        key_path = os.path.join(os.path.dirname(__file__), "key.json")
        
        spread = Spread(
            "Gehennas AH Gold Making",   # <-- REQUIRED first positional arg
            sheet="Current Price Export",
            creds=creds
        )
        spread.df_to_sheet(df, index=False, start="A1", replace=True)
        
        
if __name__ == "__main__":
    gsheet = GSheet_Controller()
    gsheet.update_cell("A1", "Yooo")  # Example update
    data = gsheet.read_all()
    print(data)
