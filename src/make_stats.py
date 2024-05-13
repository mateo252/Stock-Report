import pandas as pd
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class MakeStats():
    
    def score_by_week_day(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get profit statistics grouped by day of the week

        Args:
            df (pd.DataFrame): DataFrame with statistics from trading

        Returns:
            pd.DataFrame: statistics grouped by day of the week
        """
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                            "Friday", "Saturday", "Sunday"]
        
        # Get missing day of a week to fill it with value 0
        missing_days = list(set(days).difference(set(df["Week day"].unique())))

        df_grouped_by_day = df.groupby(["Week day"])["Net profit"].agg(["min", "max", "sum"])
        df_grouped_by_day = pd.concat([df_grouped_by_day, pd.DataFrame({"min" : 0, "max" : 0, "sum" : 0}, 
                                                                                index=missing_days)]).loc[days]
        df_grouped_by_day = df_grouped_by_day.apply(lambda x: round(x, 2))
        df_grouped_by_day.rename(columns={"min":"Min", "max":"Max", "sum":"Sum"}, inplace=True)

        return df_grouped_by_day
    
    
    def get_win_rate(self, df: pd.DataFrame) -> tuple[float, float]:
        """Calculating win and lose rate

        Args:
            df (pd.DataFrame): DataFrame with statistics from trading

        Returns:
            tuple[float, float]: rounded values of win and loss rate
        """
        
        score_counted = df["Score"].value_counts()
        win_rate = round((score_counted["Profit"]/len(df))*100, 2)
        loss_rate = round((score_counted["Minus"]/len(df))*100, 2)

        return win_rate, loss_rate
    
    
    def get_transations_number(self, df: pd.DataFrame) -> int:
        """Returns the number of transactions

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            int: number of transactions
        """
        
        return df.shape[0]    
    
    
    def get_assets(self, df: pd.DataFrame) -> pd.Series:
        """Returns a Series with the number of assets

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            pd.Series: series with counted symbols
        """
        return df["Symbol"].value_counts()
    
    
    def get_unique_assets(self, df: pd.DataFrame):
        """Returns a unique name of assets

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            unique name of assets
        """
        
        return df["Symbol"].unique()
    
    
    def get_operations_type(self, df: pd.DataFrame) -> pd.Series:
        """Returns a series with the number of transaction types

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            pd.Series: series with counted types
        """
        
        return df["Type"].value_counts()
    
    
    def get_unique_operation_types(self, df: pd.DataFrame) -> pd.Series:
        """Returns a series with the number of two transaction types (BUY/SELL)

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            pd.Series: series with counted only two types
        """
        
        return df["Type"].map(lambda x: "Sell" if "sell" in x.lower() else "Buy").value_counts()  
    
    
    def get_lot_amount(self, df: pd.DataFrame) -> pd.Series:
        """Returns a series with the number of lot types

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            pd.Series: series with counted lots
        """
        
        return df["Lots"].value_counts()
    
    
    def get_transtions_duration(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns a DataFrame with the rounded value of the transaction duration

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            pd.DataFrame: data frame with stats of deltatime
        """
        
        return pd.DataFrame({
            "Min" : round(df["Deltatime"].min(), 2), # minute
            "Max" : round(df["Deltatime"].max(), 2),
            "Sum" : round(df["Deltatime"].sum(), 2),
            "Mean" : round(df["Deltatime"].mean(), 2)
        }, index=[0]) 
        
        
    def get_profit_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns a DataFrame with the rounded profit value

        Args:
            df (pd.DataFrame): data frame with trading data

        Returns:
            pd.DataFrame: data frame with stats of profit
        """
        
        return pd.DataFrame({
            "Min" : round(df["Net profit"].min(), 2),
            "Max" : round(df["Net profit"].max(), 2),
            "Sum" : round(df["Net profit"].sum(), 2),
            "Mean" : round(df["Net profit"].mean(), 2)
        }, index=[0])
        
        
    def plot_line(self, df_data: pd.Series | np.ndarray,
                    xlabel: str, ylabel: str, title: str) -> plt.Figure: # type: ignore
        """Function generate line chart

        Args:
            df_data (pd.Series | np.ndarray): data frame with trading data to plot
            xlabel (str): name of xlabel
            ylabel (str): name of ylabel
            title (str): title of chart

        Returns:
            plt.Figure: figure of chart
        """
        
        fig, ax = plt.subplots()
        ax.plot(df_data)

        ax.grid(True, alpha=0.25)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel, labelpad=10)
        
        return fig
    
    
    def plot_bars(self, df_data: pd.Series | pd.DataFrame,
                    xlabel: str, ylabel: str, 
                    title: str, direction: str = "v") -> plt.Figure: # type: ignore
        """Function generate bar chart

        Args:
            df_data (pd.Series | np.ndarray): data frame with trading data to plot
            xlabel (str): name of xlabel
            ylabel (str): name of ylabel
            title (str): title of chart
            direction (str, optional): direction of bars - vertical/horizontal. Defaults to "v".

        Returns:
            plt.Figure: figure of chart
        """
        
        fig, ax = plt.subplots()
        
        if direction == "v":
            df_data.plot.bar(ax=ax)
            
        elif direction == "h":
            df_data.plot.barh(ax=ax)

        ax.grid(True, alpha=0.25)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel, labelpad=10)
        
        return fig
    
    
    def plot_pie(self, df_data: pd.Series | pd.DataFrame, title: str) -> plt.Figure: # type: ignore
        """Function generate pie chart

        Args:
            df_data (pd.Series | pd.DataFrame): data frame with trading data to plot
            title (str): title of chart

        Returns:
            plt.Figure: figure of chart
        """
        
        fig, ax = plt.subplots()
        df_data.plot.pie(ax=ax, autopct="%1.2f%%",
                            title=title, legend=True, 
                            labeldistance=None, shadow=True) # type: ignore
        ax.axes.get_yaxis().set_visible(False)
        
        return fig
        