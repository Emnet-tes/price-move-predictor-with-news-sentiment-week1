import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

class StockVisualization:
    """Class containing all stock visualization functions"""

    def __init__(self):
        pass

    def calculate_sma(self, df, period=20):
        """Calculate Simple Moving Average (SMA)"""
        df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
        return df

    def calculate_ema(self, df, period=50):
        """Calculate Exponential Moving Average (EMA)"""
        df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
        return df

    def calculate_rsi(self, df, period=14):
        """Calculate Relative Strength Index (RSI)"""
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df

    def calculate_macd(self, df):
        """Calculate MACD, signal line and histogram"""
        ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['Close'].ewm(span=26, adjust=False).mean()

        df['MACD'] = ema_12 - ema_26
        df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_hist'] = df['MACD'] - df['MACD_signal']
        return df

    def prepare_data(self, df):
        """Prepare DataFrame by calculating all indicators needed for plots."""
        df = df.copy()
        df = self.calculate_sma(df, period=20)
        df = self.calculate_ema(df, period=50)
        df = self.calculate_rsi(df)
        df = self.calculate_macd(df)
        return df

    def plot_stock_price(self, df, stock_name):
        """Plot stock price with moving averages"""
        plt.figure(figsize=(14, 6))
        plt.plot(df['Date'], df['Close'], label='Close Price')
        plt.plot(df['Date'], df['SMA_20'], label='SMA 20', linestyle='--')
        plt.plot(df['Date'], df['EMA_50'], label='EMA 50', linestyle=':')
        plt.xticks(df['Date'].iloc[::365])
        plt.title(f'Close Price with SMA & EMA for {stock_name}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_rsi(self, df, stock_name):
        """Plot relative strength index"""
        plt.figure(figsize=(12, 5))
        plt.plot(df['Date'], df['RSI'], label='RSI', color='purple')
        plt.xticks(df['Date'].iloc[::365*3])
        plt.yticks(range(0, 101, 10))
        plt.axhline(70, color='red', linestyle='--')
        plt.axhline(30, color='green', linestyle='--')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.title(f"Relative Strength Index (RSI) - {stock_name}")
        plt.show()

    def plot_macd(self, df, stock_name):
        """Plot moving average convergence divergence"""
        # Calculate MACD if columns don't exist
        if 'MACD' not in df.columns:
            df = self.calculate_macd(df)
            
        plt.figure(figsize=(12, 5))
        plt.plot(df['Date'], df['MACD'], label='MACD')
        plt.plot(df['Date'], df['MACD_signal'], label='Signal')
        plt.bar(df['Date'], df['MACD_hist'], label='Histogram', alpha=0.4)
        plt.xticks(df['Date'].iloc[::365*3])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.title(f"MACD & Signal Line - {stock_name}")
        plt.legend()
        plt.show()

    def plot_stock_returns(self, stock_name):
        """Plot stock returns (daily % change)"""
        stock = yf.Ticker(stock_name)
        df = stock.history(period="max").reset_index()
        returns = df['Close'].pct_change()
        returns.plot(title=f"Daily Returns - {stock_name}", figsize=(12, 5))
        plt.show()


# Example usage (outside the class):
if __name__ == "__main__":
    stock_name = "AAPL"
    stock = yf.Ticker(stock_name)
    df = stock.history(period="5y").reset_index()

    sv = StockVisualization()
    df = sv.prepare_data(df)

    sv.plot_stock_price(df, stock_name)
    sv.plot_rsi(df, stock_name)
    sv.plot_macd(df, stock_name)
    sv.plot_stock_returns(stock_name)
