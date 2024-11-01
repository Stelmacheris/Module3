import pandas as pd
from datetime import datetime
import re
import numpy as np

class TransformHandler:

    def __init__(self, df:pd.DataFrame):
        self.df = df

    def extract_date_apply(self, col: str):
        if col in self.df.columns:
            # Use Pandas to handle timezone-aware datetime strings
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce').dt.date
        else:
            print(f"Column '{col}' does not exist in the DataFrame")

    def convert_to_euro(self,value):

        usd_to_eur = 0.85
        gbp_to_eur = 1.15
    # If value has any text other than currency symbols, return np.nan
        if re.search(r'[a-zA-Z]', value) and not re.search(r'[$£]', value):
            return np.nan
        
        # Extract numeric ranges
        ranges = re.findall(r'(\d+[,\.]?\d*)', value.replace(',', ''))
        if len(ranges) == 1:
            min_val, max_val = ranges[0], ranges[0]
        elif len(ranges) > 1:
            min_val, max_val = ranges[0], ranges[1]
        else:
            return np.nan
        
        # Convert to float
        min_val = float(min_val)
        max_val = float(max_val)
        
        # Convert currency based on symbol or keyword
        if "$" in value.lower() or "usd" in value.lower():
            min_val *= usd_to_eur
            max_val *= usd_to_eur
        elif "£" in value.lower():
            min_val *= gbp_to_eur
            max_val *= gbp_to_eur
        
        # Format output
        return f"{min_val:.2f}€ - {max_val:.2f}€"
        
    def convert_to_euro_apply(self,col:str):
        self.df[col] = self.df[col].apply(self.convert_to_euro)

    def get_df(self):
        return self.df