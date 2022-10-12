import imp
from pprint import pprint
from turtle import color
from utils.config import *
from copy import deepcopy
from utils.trading_utils import model_to_signal, load_strategy
import os
import matplotlib.pyplot as plt
from utils.datasets import load_ETHUSD_2021
from red_panda.utils.generator import *


def backtest(df , trading_strategy, equity=100_000,print_operations=False):
    """ df pd.DataFrame()
    Columns ['open', 'high', 'low', 'close', 'volume', 'signal']
    datetime as Index
    """  
    LAVERAGE = 10
    initial_investment = equity
    open_operation = False
    max_drawdown = 0.5
    id_op = 0 # id of operation
    gain = 0 # gain of operation
    equity_history=[]
    sympy_tp_sl = pd.DataFrame()
    counter_errors_model_to_signal = 0

    actual_equity = (equity + gain) 

    # if 'take_profit' in trading_strategy:
    #     take_profit =  float(trading_strategy['take_profit'])

    # if 'stop_loss' in trading_strategy:
    #     stop_loss = float(trading_strategy['stop_loss'])

    for i in range(buffer_period):
        equity_history.append(equity)

    #plt.ion()
    
    #sl_eq = trading_strategy['stop_loss']['equation']
    tp_eq = float(trading_strategy['take_profit'])#['equation']

    logic = trading_strategy['logic']
    for idx in trading_strategy['equations'].keys():
        if markup_sympy not in idx:
            logic = trading_strategy['logic'].replace( idx , name_df_ram + "['" + str(idx+markup_sympy) + "']" )
    #trading_strategy['logic'] = "(final_df['sd-10-@']  >  final_df['sd-31-@'] ) and (ema-42-@ < final_df['ema-22-@'])"
    pprint(trading_strategy)
    
    signal = np.array([0,0])
    
    signal, math_indicators = model_to_signal(df, trading_strategy)
    
    sympy_tp = subtitute_expression_to_index(n1(df['close']) , tp_eq)

    # for i in math_indicators.columns:
    #     if i not in trading_strategy['logic']:
    #         del math_indicators[i]

    for i in range(buffer_period, len(df)):
        if equity <= initial_investment * (1 - max_drawdown):
            break
        
        #print(logic_eval)
        #print(signal.value_counts())
        # except:
        #     signal = np.empty(2)
        #     counter_errors_model_to_signal+=1
        #     SUCCESS = False
        #     continue
        #sympy_sl = subtitute_expression_to_index(n1(df['close'][i-200:i]) , sl_eq)

        position_book = {'1':0, '2':0, '3':0,'4':0, '5':0}
        os.system('clear')

        if not open_operation:
            if signal.any():
                if signal[-1]:
                    # Open Long position #####
                    open_operation = True
                    id_op += 1
                    op_open_price = df['close'][i]
                    op_open_date = df.index[i]
                    size_order = equity / df['close'][i] * LAVERAGE
                    volatility_factor = df['close'][-200:].std() / 10
                    take_profit = sympy_tp[-1] / 10 * volatility_factor                    
                    stop_loss = 0.03/LAVERAGE
                    while take_profit > 0.16/LAVERAGE:
                        take_profit = take_profit / 10

                    take_profit_price = op_open_price + take_profit * op_open_price
                    stop_loss_price = op_open_price - (stop_loss * op_open_price )                    
                    take_profit_equity = take_profit_price * size_order
                    stop_loss_equity = stop_loss_price * size_order
                    tp_gain = take_profit_equity-actual_equity * LAVERAGE
                    sl_loss = stop_loss_equity-actual_equity * LAVERAGE


                    #if str(sympy_tp_sl['tp'].iloc[-1]) == 'nan' or str(sympy_tp_sl['sl'].iloc[-1]) == 'nan' :
                    #take_profit = float(trading_strategy['take_profit']['default']) * volatility_factor
                    #stop_loss = float(trading_strategy['stop_loss']['default']) * volatility_factor

        actual_price = df['close'][i] 

        print('equity ', round(equity,2),' $')       
        print('gain ',round(gain,2),' $')
        print(trading_strategy['logic'])
        print(df.index[i])
        print(float(math_indicators.iloc[i].values[0]),' < ',float(math_indicators.iloc[i].values[1]))
        print(signal[i])
        print('\n')

        if print_operations and open_operation:
            print(' ID operation\t ',id_op)
            print(' entry date  \t',op_open_date)
            print(' entry price \t',op_open_price)
            print(' actual price\t',actual_price)
            print(' TP exit price\t',round(take_profit_price,5)) 
            print(' SL exit price\t',round(stop_loss_price,5) )
            print(' TP USD gain\t',round(tp_gain,2) )
            print(' SL USD loss\t',round(sl_loss,2) )
            print(' TP exit equity\t',round(take_profit_equity,5)) 
            print(' SL exit equity\t',round(stop_loss_equity,5) )
            print(' size order  \t',round(size_order,5))
            print(' TP %        \t',round(take_profit*100,2))
            print(' SL %        \t',round(stop_loss*100,2))
            print(' gain $      \t',round( gain ,2))
            print(' equity $    \t',round( actual_equity ,2))
            print(" take_profit \t",take_profit)
            print(" stop_loss   \t",stop_loss)

        if open_operation:
            gain =  size_order * (actual_price - op_open_price)  # LONG or use  (op_open_price - actual_price) for SHORT
            actual_equity = (equity + gain) 
        
            if take_profit_price <= actual_price or actual_price <= stop_loss_price:
                equity += gain
                open_operation = False
                gain = 0





        equity_history.append(equity + gain)

        if equity  < initial_investment * (1-max_drawdown):
            print('Max drawdown reached')
            break

    #     plt.plot(range(300),df['close'].iloc[i-300:i] , color ='blue')

    #     if open_operation:
    #         plt.axhline(y = op_open_price , color = 'black', linestyle = '--')
    #         plt.axhline(y = take_profit_price, color = 'lime', linestyle = '--')
    #         plt.axhline(y = stop_loss_price, color = 'red', linestyle = '--')

    #     plt.title('Backtester', color='black', fontsize=20, fontweight='bold')
    #     plt.xlabel("ticks")
    #     plt.draw()
    #     plt.pause(0.03)
    #     plt.clf()       

    # plt.show(block=True)

    return equity_history


def from_raw_signal_to_signal(raw_signal):
    open_signal = []
    close_signal = []

    for i in range(1,len(raw_signal)):
        if raw_signal[i] == True and raw_signal[i-1] == False:
            open_signal.append(True)

        if raw_signal[i] == False and raw_signal[i-1] == True:
            close_signal.append(False)
        
        if raw_signal[i] == False and raw_signal[i-1] == False:
            open_signal.append(None)
            close_signal.append(None)

        if raw_signal[i] == True and raw_signal[i-1] == True:
            open_signal.append(None)
            close_signal.append(None)

    return np.array(open_signal), np.array(close_signal) 