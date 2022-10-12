"""
take bot parameter as an input and return python file for trading
"""

# read file
# place strategy as a function
# write file .py

#from cProfile import label
from cProfile import label
import os

#from get_datastream_truefx import DATA_FILE_NAME
import matplotlib.pyplot as plt
import time
import pandas_ta as ta
from colored import fg, bg, attr

# COLORS 
red_color = fg('red') #+ bg('black') 
yellow = fg('yellow')
green_color = fg('green') #+ bg('black') 
blue_color = fg('#15a6dc')
res = attr('reset')

from model_generator import *
from utils.config import *
from utils.trading_utils import *

def trader_logo():
    print(red_color+"""                                                                                                            
    __                       
    | \ _ ._ _  _ ._  |_|   .__|_ _ ._                   
    |_/(/_| | |(_)| | | ||_|| ||_(/_|
         redpanda paper trading   
    """+res)


if __name__ == '__main__':
    

    strategy = load_strategy(MODEL_PATH_daemon_hunter)

    max_window_required = compute_max_window_required(strategy)   # max window required for all equations
    TAIL_NUMBER = max_window_required+20 # number of points to plot

    plt.ion()    
    while True:

        df = pd.read_csv(DATA_FILE_NAME, index_col=0, parse_dates=True)
        #df.index = df.index.tz_convert('Europe/Paris')

        signal, df_strategy_indicators = model_to_signal(df = df, model=strategy)

        #df_signal = pd.read_csv(DATA_FILE_NAME, index_col=0, parse_dates=True)
        row = str(df.index[-1]) +','+ str(df['close'][-1])+','+str(signal[-1])

        with open(DATA_FILE_NAME_SIGNAL, "a") as f:
            f.write(row+'\n')
            f.close()

        os.system('clear')

        trader_logo()
        print(f"\t last price: {df['close'][-1]}\n\t date time: {df.index[-1]}\n\t price data path: {DATA_FILE_NAME}\n\t model path: {MODEL_PATH} \n\n")

        if signal[-1] == True:
            print('\t signal: ',green_color,'[ LONG ]',res)

        else:
            print('\t signal: ',yellow,'[ stay ]',res)

        df_signal_plot = pd.read_csv(DATA_FILE_NAME_SIGNAL, index_col=0, parse_dates=True,header=0)


        df_signal_plot.index = df_signal_plot.index.tz_localize('UTC')
        
        df_plot_only_important_indicators = pd.DataFrame()
        for idx in df_strategy_indicators.columns:
            if str(idx) in strategy['logic']:
                df_plot_only_important_indicators[idx] = df_strategy_indicators[idx]
        
        plt.plot( df_plot_only_important_indicators[-TAIL_NUMBER:])
        plt.legend(df_plot_only_important_indicators.columns)
        plt.plot( df_signal_plot['signal'][-TAIL_NUMBER:], color='indigo')
        plt.title('Trading strategy signal ', color='darkblue')
        plt.suptitle('logic: '+strategy['logic'].replace(markup_sympy,''), color='black')
        plt.xlabel("datetime")
        plt.legend(df_plot_only_important_indicators.columns)
        plt.draw()
        plt.pause(0.1)
        plt.clf()

        time.sleep(5)

    plt.show(block=True)
