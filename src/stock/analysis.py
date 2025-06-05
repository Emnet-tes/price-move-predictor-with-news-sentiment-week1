"""Stock analysis class - contains all stock analysis functions"""

import pandas as pd
import pandas_ta as ta


class StockAnalysis:
    """Class containing all stock analysis functions"""

    def __init__(self):
        pass

    def load_stock_data(self, stock_name):
        """
        Load stock data
        """
        file_path = f'../data/{stock_name}_historical_data.csv'
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    def calculate_moving_averages(self, df, short_window=20, long_window=50):
        """
        Calculate moving averages using pandas_ta
        """
        df['SMA_20'] = df.ta.sma(length=short_window)
        df['EMA_50'] = df.ta.ema(length=long_window)
        return df
    
    def calculate_rsi(self, df, period=14):
        """
        Calculate relative strength index using pandas_ta
        """
        df['RSI'] = df.ta.rsi(length=period)
        return df
    
    def calculate_macd(self, df):
        """
        Calculate MACD using pandas_ta
        """
        macd = df.ta.macd()
        df = pd.concat([df, macd], axis=1)
        return df
