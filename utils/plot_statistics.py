import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.config import ROOT_PATH
from utils.config import number_of_plots
from utils.config import experiment_number


def plot_equity_curve(df, n_points_plot = 200):
    """
    plot equity curve with trading strategy
    and with a restricted number of points n_points_plot = 200
    due to graphical requirements
    """
    idx = list(range( 0 ,len(df['trading strategy']), math.floor(len(df['trading strategy'])/n_points_plot) ))
    trading_strategy_gain = [df['trading strategy'][i] for i, _ in enumerate(df['trading strategy']) if i in idx][1:]
    plt.plot(trading_strategy_gain)
    plt.savefig(f"{ROOT_PATH}/runs/experiment_{experiment_number}/bot_{number_of_plots}_equity.png")
    plt.show()


def plot_indicators(df,title='title'):
    figure, axis = plt.subplots(len(list(df.columns)), 1,figsize=(16, 10))

    for idx in range(len(df.columns)):
        axis[idx].plot(df[df.columns[idx]].tail(200),color='red')
        axis[idx].set_title(df.columns[idx])
        axis[idx].set(xticklabels=[])

    plt.title(title)
    plt.savefig(f"{ROOT_PATH}/runs/experiment_{experiment_number}/bot_{number_of_plots}_indicators.png")
    plt.show()


def plot_price_and_signal(price, signal, open_signal  = None, close_signal = None ):
    # plot the trading strategy
    plt.figure(figsize=(25,15))
    
    number_of_points = 300 

    idx = list(range( 0 ,len(price), math.floor(len(price)/number_of_points) ))
    price_array_reduced = [price[i] for i, _ in enumerate(price) if i in idx][1:]
    signal_array_reduced = [signal[i] for i, _ in enumerate(price) if i in idx][1:]

    plt.clf()
    plt.style.use('seaborn-pastel')
    plt.plot(price_array_reduced,color='darkblue')
    plt.plot(range(len(pd.Series(signal_array_reduced))), pd.Series(signal_array_reduced).map({False:min(price),True:max(price)}) , color='green', label='buy',alpha=0.75 )
    plt.legend(['EURUSD price','trading strategy signal'],colors=['darkblue','purple'])      
    plt.format_xdata = mdates.DateFormatter('%m %d')
    plt.xlabel('time: 1 year (2021)', fontsize = 13)
    plt.ylabel('EURUSD price', fontsize = 13)
    plt.gcf().autofmt_xdate()
    plt.title("Trading signal and Asset price  ")
    plt.savefig(f"{ROOT_PATH}/runs/experiment_{experiment_number}/bot_{number_of_plots}_signal.png")
    plt.show()

def plot_strategy_vs_benchmark(trading_strategy, benchmark, signal):      
    number_of_points = 300 
    idx = list(range( 0 ,len(trading_strategy), math.floor(len(signal)/number_of_points) ))
    trading_strategy_reduced = [trading_strategy[i] for i, _ in enumerate(trading_strategy) if i in idx][1:]
    signal_array_reduced = [trading_strategy[i] for i, _ in enumerate(trading_strategy) if i in idx][1:]
    benchmark_reduced = [trading_strategy[i] for i, _ in enumerate(trading_strategy) if i in idx][1:]
    
    plt.figure(figsize=(25,15))
    plt.clf()
    plt.style.use('seaborn-pastel')

    plt.plot(trading_strategy_reduced , color='purple')
    plt.plot(benchmark_reduced , color='purple')
    plt.plot(range(len(pd.Series(signal_array_reduced))), pd.Series(signal_array_reduced).map({False:min(trading_strategy),True:max(trading_strategy)}) , color='green', label='buy',alpha=0.75 )
    plt.legend(['trading strategy','benchmark_reduced','signal'])
    plt.format_xdata = mdates.DateFormatter('%m %d')
    plt.xlabel('time: 1 year (2021)', fontsize = 13)
    plt.ylabel('investment: USD $', fontsize = 13)
    plt.gcf().autofmt_xdate()
    plt.xticks(np.arange(0, len(trading_strategy), 20),rotation=40, fontsize=10)
    plt.title(" trading strategy EURUSD  VS  benchmark SNP500")
    plt.suptitle(f"generated strategy experiment number :{experiment_number} robot number : {number_of_plots}")
    plt.savefig(f"{ROOT_PATH}/runs/experiment_{experiment_number}/bot_{number_of_plots}_ts_vs_benchmark.png")
    plt.show()


def plot_gains(df_trading, df_benchmark):
    plt.figure(figsize=(15,8))
    plt.hist(df_benchmark['Daily Return']*100 , bins=20, alpha=0.8, label='benchmark',color='blue')
    plt.hist(df_trading['Daily Return']*100 , bins=30, alpha=0.4, label='trading strategy',color='green')
    plt.legend(loc='upper right')
    plt.xlabel("daily returns %")
    plt.ylabel("")
    plt.title("Portfolio returns vs Benchmark returns")
    plt.savefig(f"{ROOT_PATH}/runs/experiment_{experiment_number}/bot_{number_of_plots}_gains.png")
    plt.show()

