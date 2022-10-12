import random as rnd
from copy import deepcopy
import time
import math
from pprint import pprint
import numpy as np
import pandas as pd
import pandas_ta as ta
from utils.config import *
from model_generator import *

if __name__ == "__main__":

    for n_generation in range(2,len(GENERATIONS)+1):        
        CHILDRENS = deepcopy(POPULATION)
        
        # cross over
        for child_id in range(len(CHILDRENS)):
            CROSS_OVER_RATE = CHILDRENS[child_id]['shape_rateo']
            if rnd.random()>CROSS_OVER_RATE:
                CHILDRENS[child_id] = cross_over(CHILDRENS[child_id])

        # mutate
        for child_id in range(len(CHILDRENS)):
            if rnd.random()>MUTATION_RATE:
                CHILDRENS[child_id] = mutate(CHILDRENS[child_id])
    
        # selection
        for n_element in range(1,len(POP_SIZE)+1):
            take_profit = CHILDRENS[n_element]['take_profit']
            stop_loss = CHILDRENS[n_element]['stop_loss']
            indicators = CHILDRENS[n_element]['equations'].keys()
            
            new_df = pd.DataFrame()
            
            for indicator in indicators:
                new_df[indicator] = compute_financial_indexes(df,indicator)

            #sympy_df, equations = math_generator( seed_df = new_df, indicators_list = indicators )
            
            final_df = pd.DataFrame()

            normalization_methods = {}
            for idx in sympy_df.columns:
                normalization_method = available_normalizations[rnd.randint(0,len(available_normalizations)-1)]
                final_df[idx] = pd.Series(apply_normalization( sympy_df[idx] , normalization_method))
                normalization_methods[idx] = normalization_method

            time.sleep(0.3)
            
            signal = np.array([])
            logic = CHILDRENS[n_element]['logic']
            try:
                signal = eval(logic) # EVALUATION 
            except:
                pass
                
            if signal.any():

                df['signal'] = signal
                df['backtest'] = backtest( df ) # DEPLOY

                # STATISTICS: shape rateo
                if df['backtest'][-1] != df['backtest'][0]:

                    idx = list(range( 0 ,len(df['backtest']), math.floor(len(df['backtest'])/n_points_plot) ))
                    trading_strategy_gain = [df['backtest'][i] for i, _ in enumerate(df['backtest']) if i in idx][1:]
                    
                    df_trading = pd.DataFrame()
                    df_trading['trading strategy'] = trading_strategy_gain
                    df_trading['Daily Return'] = df_trading['trading strategy'].pct_change() 
                    df_trading.dropna(inplace=True)

                    shape_rateo_trading_strategy = sharpe_ratio(df_trading['Daily Return'],risk_free_rate=0.00)
                    
                    if shape_rateo_trading_strategy > shape_rateo_benchmark*0.5:
                        POPULATION.append(TRADING_RULES)

                        TRADING_RULES = {"logic" : logic_str ,
                                        "equations" : str(equations),
                                        "normalization_methods" : normalization_methods,
                                        "take_profit" : take_profit,
                                        "stop_loss" : stop_loss,
                                        "fitness":shape_rateo_trading_strategy,
                                        "shape_rateo" : shape_rateo_trading_strategy}
            
                        print('\nNEW TRADING STRATEGY!')   
                        print('shape rateo ', shape_rateo_trading_strategy )
                        pprint(TRADING_RULES,'\n')
