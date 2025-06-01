import pandas as pd
import numpy as np
from finance_fns import stock_handle
from finance_fns.stock_handle import get_close_df, add_to_df


def macd_oscillator(stock_code: str, start_date: str, short_n: int, long_n: int, signal_n: int) -> pd.DataFrame:
    df_close = get_close_df(stock_code, start_date)

    add_index = add_to_df(df_close)
    add_index('Short', lambda df: df['Close'].ewm(span=short_n, adjust=False).mean())
    add_index('Long', lambda df: df['Close'].ewm(span=long_n, adjust=False).mean())
    add_index('MACD', lambda df: df['Short'] - df['Long'])
    add_index('Signal', lambda df: df['MACD'].ewm(span=signal_n, adjust=False).mean())
    final_df = add_index('MACD_Oscillator', lambda df: df['MACD'] - df['Signal'])

    return final_df[['MACD', 'Signal', 'MACD_Oscillator']]


def rsi_df(stock_code, start_date='2024', rsi_period=14) -> pd.DataFrame:
    df_close = stock_handle.get_close_df(stock_code, start_date=start_date)
    add_index = stock_handle.add_to_df(df_close)
    add_index('change', lambda df: df['Close'] - df['Close'].shift(1))
    add_index('gain', lambda df: np.where(df['change'] >= 0, df['change'], 0))
    add_index('loss', lambda df: np.where(df['change'] < 0, -df['change'], 0))
    add_index('avg_gain', lambda df: df['gain'].rolling(rsi_period).mean())
    add_index('avg_loss', lambda df: df['loss'].rolling(rsi_period).mean())
    final_df = add_index('rsi', lambda df: 100 - (100 / (1 + df['avg_gain'] / df['avg_loss'])))
    return final_df[['rsi']]



def dd_df(stock_code) -> pd.DataFrame:
    df_close = stock_handle.get_close_df(stock_code, start_date='2024')

    add_index = stock_handle.add_to_df(df_close)
    add_index('Return', lambda df: df['Close'].pct_change().fillna(0))
    add_index('CumReturn', lambda df: (1 + df['Return']).cumprod())
    add_index('MaxCumReturn', lambda df: df['CumReturn'].cummax())
    df = add_index('DrawDown', lambda df: (df['CumReturn'] /df['MaxCumReturn']) -1)
    mdd = df['DrawDown'].min()



