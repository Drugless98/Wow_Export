
import os

class QueriesController:
    def __init__(self):
        self.Qpath = os.path.join(os.path.dirname(__file__), "Query_files")
        
    def get_Query(self, queryfile_name: str):
        try:
            with open(f"{self.Qpath}\\{queryfile_name}.sql", "r") as QFile:
                return QFile.read()
        except Exception as e:
            print(e)
            return None