import pandas as pd
from dataclasses import dataclass


@dataclass
class DataReader():

    def load_file(self, uploaded_file) -> pd.DataFrame:
        """Function to load csv to DataFrame

        Args:
            uploaded_file: csv file with data 

        Returns:
            pd.DataFrame: loaded csv file to DataFrame
        """
        
        return pd.read_csv(uploaded_file, sep=";", decimal=".") \
                .sort_values(by="Close time") \
                .reset_index(drop=True)
                                    
        
    def rename_header(self, df: pd.DataFrame, new_header: dict) -> pd.DataFrame:
        """Function to change the headers of a data frame

        Args:
            df (pd.DataFrame): data frame to edit
            new_header (dict): header name to edit

        Returns:
            pd.DataFrame: data frame with new header name
        """
        
        return df.rename(columns=new_header)
    
    
    def format_data_frame(self, df: pd.DataFrame, date_format: str|None, balance: float) -> pd.DataFrame:
        """Function adjusts all the most important elements of the data frame

        Args:
            df (pd.DataFrame): data frame to edit
            date_format (str): date format to set new format
            balance (float): starting value of account

        Returns:
            pd.DataFrame: final version of the data frame
        """

        # Formating date to selected format
        df["Close time"] = pd.to_datetime(df["Close time"], format=date_format)
        df["Open time"]  = pd.to_datetime(df["Open time"],  format=date_format)
        
        day = {
            0 : "Monday",
            1 : "Tuesday",
            2 : "Wednesday",
            3 : "Thursday",
            4 : "Friday",
            5 : "Saturday",
            6 : "Sunday"
        }
        # Get day of the week
        df["Week day"] = df["Close time"].dt.date.map(lambda x: x.weekday()).map(day)
        
        # Set balance of account after closed transaction
        df["Balance"] = balance
        df.loc[0, "Balance"] = df["Balance"][0] + df["Net profit"][0]

        for i in range(1, df.shape[0]):
            df.loc[i, "Balance"] = df["Balance"][i-1] + df["Net profit"][i]
            
        # Calcutalte of session time in minutes
        df["Deltatime"] = (df["Close time"] - df["Open time"])
        df["Deltatime"] = df["Deltatime"].dt.total_seconds()/60 # minute
        
        # Check if transaction was succes or fail
        df["Score"] = df["Net profit"].map(lambda x: "Minus" if x < 0 else "Profit")
        
        return df
    