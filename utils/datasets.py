from utils.config import *
import pandas as pd

def load_ETHUSD_2021():
    df = pd.read_csv(DATA_FILE_NAME_ETHUSD_1m_2021,skiprows=0)# index_col=['date'])#,parse_dates=['date'])
    del df['unix']
    del df['symbol']
    del df['Volume ETH']
    df.sort_values(by=['date'], inplace=True, ascending=True)
    df = df.set_index('date')
    df.rename({'Volume USD': 'volume'},axis=1, inplace=True)
    return df

def load_EURUSD_1m_2022():
    df = pd.read_csv( DATA_FILE_NAME_EURUSD_1m_2022 ,skiprows=0)
    df.sort_values(by=['date'], inplace=True, ascending=True)
    df = df.set_index('date')
    return df


def load_benchmark():
    df_benchmark = pd.read_csv(  DATA_FILE_NAME_BENCHMARK, index_col=0)
    df_benchmark.sort_values(by=['Date'], inplace=True, ascending=True)
    final_df = df_benchmark.rename(columns={'Close':'close','Open':'open','High':'high','Low':'low'})
    return final_df
