# Import Modules
import pandas as pd
import numpy as np

#Modules for Yahoo!Finance
from pandas_datareader import data as pdr
import yfinance as yf


# Import the finta library
from finta import TA

def get_historical_data(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol)
    ticker_df = ticker.history(start=start_date, end=end_date)
    return ticker_df

def get_data(tickers, start_date, end_date):
    df = yf.download(tickers, start_date, end_date)
    df['Source'] = 'Yahoo'
    return df[['Open','High','Low','Close','Adj Close','Volume','Source']]

def get_returns(df):
    # Filter the date index and close columns
    _df  = df.loc[:, ["Close"]]

    # Use the pct_change function to generate  returns from close prices
    _df["Actual Returns"] = _df["Close"].pct_change()
    
    # Drop all NaN values from the DataFrame
    _df = _df.dropna()
    return _df

def create_sma (df, short_window, long_window):
    # Generate the fast and slow simple moving averages (4 and 100 days, respectively)
    df['SMA_Fast'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_Slow'] = df['Close'].rolling(window=long_window).mean()
    
    return df

def create_signal_using_sma(df):
    # Initialize the new Signal column
    df['Signal'] = 0.0

    # When Actual Returns are greater than or equal to 0, generate signal to buy stock long
    df.loc[(df['Actual Returns'] > 0), 'Signal'] = 1

    # When Actual Returns are less than 0, generate signal to sell stock
    df.loc[(df['Actual Returns'] < 0), 'Signal'] = -1
    
    return df


def create_bollinger_bands(df):
    
    # Determine the Bollinger Bands for the Dataset
    bbands_df = TA.BBANDS(df)
    return bbands_df


def create_signal_using_bollinger(df):
    # Create a trading algorithm using Bollinger Bands
    # Set the Signal column
    df["Signal"] = 0.0

    # Generate the trading signals 1 (entry) or -1 (exit) for a long position trading algorithm
    # where 1 is when the Close price is less than the BB_LOWER window
    # where -1 is when the Close price is greater the the BB_UPPER window
    for index, row in df.iterrows():
        if row["close"] < row["BB_LOWER"]:
            df.loc[index, "Signal"] = 1.0
        if row["close"] > row["BB_UPPER"]:
            df.loc[index,"Signal"] = -1.0

    return df