import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.Database import Postgress
from DataAnalysis.Queries import QueriesController

from datetime import datetime
import numpy as np

class Controller:
    def __init__(self):
        print("Making initial values")
        self.DB      = Postgress()
        self.Queries = QueriesController()
        print("done with Init")

    def make_avgDay_price(self):
        tableData = self.DB.get_table_data(self.Queries.get_Query("PerDay_TotalTradeskill"))
        perDay = np.array(tableData)
        return perDay
    
    def make_graph(self,
        X: list,
        Y: list,
        label: str,
        XLabel: str,
        YLabel: str,
        Title: str,
        grid: bool = True,
        show_all_x: bool = False,):
        import numpy as np
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        ax.plot(X, Y, label=label)
        ax.set_xlabel(XLabel)
        ax.set_ylabel(YLabel)
        ax.set_title(Title)
        ax.grid(grid)

        if show_all_x:
            # If X is strings (categorical), place ticks at 0..N-1 and label them
            if len(X) and isinstance(X[0], str):
                ax.set_xticks(np.arange(len(X)))
                ax.set_xticklabels(X, rotation=45, ha="right")
            else:
                # Numeric or datetime — use X directly
                ax.set_xticks(X)
                ax.tick_params(axis='x', labelrotation=45)

        if label:
            ax.legend()

        fig.tight_layout()
        plt.show()

        
        

if __name__ == "__main__":
    import json
    c = Controller()
    perDay = c.make_avgDay_price()
    
    c.make_graph(perDay[:,0], perDay[:,1], "label?", "Days", "Tradegoods Value", "Tradegoods Avg. Prices",show_all_x=True )
    
c
    