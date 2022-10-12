import os
import random as rnd
import time
import math
from pprint import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colored import fg, attr

# COLORS 
red_color = fg('red')
yellow = fg('yellow')
green_color = fg('green') 
blue_color = fg('#15a6dc')
res = attr('reset')

from utils.config import *
from utils.backtest import *
from utils.datasets import *
from red_panda.utils.generator import *
from utils.performance import *
from utils.plot_statistics import *
from utils.save_model import *

def logo():
    print(f""" {red_color}
     _____          _   _____                _        
    |  __ \        | | |  __ \              | |       
    | |__) |___  __| | | |__) |_ _ _ __   __| | __ _  
    |  _  // _ \/ _` | |  ___/ _` | '_ \ / _` |/ _` | 
    | | \ \  __/ (_| | | |  | (_| | | | | (_| | (_| | 
    |_|  \_\___|\__,_| |_|   \__,_|_| |_|\__,_|\__,_|

              quantitative model generator   
                    created by erma0x       
          {res}""")

def generate_model():
    take_profit = rnd.choice(gabmling_space)
    stop_loss = rnd.choice(gabmling_space)
    

    indicators = random_indicators( num = 5 )
    
    new_df = pd.DataFrame()

    for indicator in indicators:
        new_df[indicator] = compute_financial_indexes(df,indicator)
        
    sympy_df, equations = math_generator( seed_df = new_df, indicators_list = indicators )
    
    signal_df = pd.DataFrame()
    normalization_methods = {}
    for idx in sympy_df.columns:
        normalization_method = available_normalizations[rnd.randint(0,len(available_normalizations)-1)]
        signal_df[idx] = pd.Series(apply_normalization( sympy_df[idx] , normalization_method))
        normalization_methods[idx] = normalization_method

    for idx in signal_df.columns:
        signal_df[idx] = n1(sympy_df[idx])

    for idx in signal_df.columns:
        if not signal_df[idx].any():
            del signal_df[idx]
            del normalization_methods[idx]
            del equations[idx.replace(markup_sympy,'')]

    logic = generate_logic_rules(dataframe_name = name_df_ram ,names = signal_df.columns)

    TRADING_RULES = {"logic" : logic ,
                    "equations" : equations,
                    "normalization_methods" : normalization_methods,
                    "take_profit" : take_profit,
                    "stop_loss" : stop_loss} 

    return TRADING_RULES, signal_df

if __name__ == "__main__":
    logo()

    df = load_ETHUSD_2021()

    df_benchmark = load_benchmark()
    number_of_shares =  initial_amout / df_benchmark['Close'][0]
    benchmark_investment =  number_of_shares * df_benchmark['Close']
    df_benchmark['Daily Return'] = benchmark_investment.pct_change() 
    df_benchmark.dropna(inplace=True)
    shape_rateo_benchmark = sharpe_ratio(df_benchmark['Daily Return'] , risk_free_rate=0.0)

    while os.path.exists(f"{ROOT_PATH}/runs/experiment_{experiment_number}"):
        experiment_number+=1

    if not os.path.exists(f"{ROOT_PATH}/runs/experiment_{experiment_number}"):
        os.makedirs(f"{ROOT_PATH}/runs/experiment_{experiment_number}")

    POPULATION = []
    while len(POPULATION) < POP_SIZE:
        
        model, signal_df = generate_model()
        SIGNAL = np.array([0,0])
        print(signal_df.tail(1))
        print(model['logic'])

        try:
            SIGNAL  = eval(model['logic'])
        except ValueError:
            print('Use a.empty, a.bool(), a.item(), a.any() or a.all()')
   

        os.system('clear')
        
        logo()
        n_element += 1

        print(f"\n\tdead 🪦    [ {n_element-len(POPULATION)} ]")
        print(f"\n\talive ⚕️   [ {len(POPULATION)} ]")
        print(f"\n\tsurvival  [ {round(len(POPULATION)/(n_element+len(POPULATION)),4)*100} ] %\n\n")

        if SIGNAL.any():
            print('strategy found')
            df['signal'] = SIGNAL
            print(df['signal'].value_counts())

            if df['signal'] .value_counts(True)[0] > 0.01 and df['signal'] .value_counts(True)[0] < 0.99:
                df['trading strategy'] = backtest( df , model)
                idx = list(range( 0 ,len(df['trading strategy']), math.floor(len(df['trading strategy'])/n_points_plot) ))
                trading_strategy_gain = [df['trading strategy'][i] for i, _ in enumerate(df['trading strategy']) if i in idx][1:]
                df_trading = pd.DataFrame()
                df_trading['trading strategy'] = trading_strategy_gain
                df_trading['Daily Return'] = df_trading['trading strategy'].pct_change() 
                df_trading.dropna(inplace=True)
                shape_rateo_trading_strategy = sharpe_ratio(df_trading['Daily Return'],risk_free_rate=0.00)
                print('shape rateo ',shape_rateo_trading_strategy)

                if shape_rateo_trading_strategy > SELECTION_FITNESS_FIRST_GEN:

                    save_parameters(input_text = str(model).replace("'",'"'))
                    number_of_plots+=1
                    POPULATION.append(model)
                    print(f'population size {len(POPULATION)}')
                    print(f'shape rateo {round(shape_rateo_trading_strategy,4)}\n')
                    pprint(model)
                    time.sleep(5)
