import pandas as pd
import re
import numpy as np

class TransformHandler:
    """
    A class to perform data transformations on a Pandas DataFrame, 
    including extracting dates and converting currency values to Euros.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing data to be transformed.

    Methods:
    --------
    extract_date_apply(col: str):
        Extracts and converts datetime strings to date format in the specified column.

    convert_to_euro(value: str):
        Converts a currency range string (in USD or GBP) to a Euro range.
    
    convert_to_euro_apply(col: str):
        Applies the `convert_to_euro` method to all entries in the specified column.
    
    get_df():
        Returns the transformed DataFrame.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes TransformHandler with a DataFrame.

        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame containing data to transform.
        """
        self.df = df

    def extract_date_apply(self, col: str):
        """
        Extracts the date component from timezone-aware datetime strings in the specified column.
        
        Parameters:
        -----------
        col : str
            The name of the column to apply date extraction.

        Raises:
        -------
        ValueError
            If the column is missing, a message is printed, and no transformation is applied.
        """
        if col in self.df.columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce').dt.date
        else:
            print(f"Column '{col}' does not exist in the DataFrame")

    def convert_to_euro(self, value: str):
        """
        Converts a currency range string (e.g., "$1000 - $2000" or "£800 - £1500") to a Euro range.
        
        Parameters:
        -----------
        value : str
            Currency range in USD or GBP format.

        Returns:
        --------
        str or NaN
            A Euro range string if conversion is successful, or NaN if the value cannot be converted.
        """
        usd_to_eur = 0.85
        gbp_to_eur = 1.15

        if re.search(r'[a-zA-Z]', value) and not re.search(r'[$£]', value):
            return np.nan

        ranges = re.findall(r'(\d+[,\.]?\d*)', value.replace(',', ''))
        if len(ranges) == 1:
            min_val, max_val = ranges[0], ranges[0]
        elif len(ranges) > 1:
            min_val, max_val = ranges[0], ranges[1]
        else:
            return np.nan

        min_val = float(min_val)
        max_val = float(max_val)

        if "$" in value.lower() or "usd" in value.lower():
            min_val *= usd_to_eur
            max_val *= usd_to_eur
        elif "£" in value.lower():
            min_val *= gbp_to_eur
            max_val *= gbp_to_eur

        return f"{min_val:.2f}€ - {max_val:.2f}€"

    def convert_to_euro_apply(self, col: str):
        """
        Applies currency conversion to Euro for all entries in the specified column.
        
        Parameters:
        -----------
        col : str
            The column containing currency values to convert.
        """
        self.df[col] = self.df[col].apply(self.convert_to_euro)

    def get_df(self):
        """
        Returns the transformed DataFrame.

        Returns:
        --------
        pd.DataFrame
            The DataFrame after applying transformations.
        """
        return self.df
