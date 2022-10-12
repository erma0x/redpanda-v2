import json
from numba import jit

from red_panda.utils.generator import *

#@jit
def model_to_signal(df, strategy):
    df.ta.cores = 4

    if 'logic' in strategy:
        logic = strategy['logic']

    if 'equations' in strategy:
        equations = strategy['equations']

    if 'normalization_methods' in strategy:
        normalization_methods = strategy['normalization_methods']

    new_df = pd.DataFrame()
    signal_df = pd.DataFrame()

    for indicator in equations.keys():
        signal_df[indicator+markup_sympy] = compute_financial_indexes(df ,indicator)

    #print(new_df.tail(1))

    # sympy_df = pd.DataFrame()

    # for idx in equations.keys():
    #     equation = equations[idx]['equation']
    #     sympy_df[idx+markup_sympy] = subtitute_expression_to_index(new_df[idx], equation)
    
    # #print(sympy_df.tail(1))


    # for idx in sympy_df.columns:
    #     normalization_method = normalization_methods[idx] 
    #     signal_df[idx] = pd.Series(apply_normalization( sympy_df[idx] , normalization_method))

    # #print(signal_df.tail(1))

    # for idx in signal_df.columns:
    #     signal_df[idx] = n1(sympy_df[idx])

    #print(signal_df.tail(1))

    logic_eval = logic

    for idx in signal_df.columns:
        if markup_sympy not in idx:
            logic_eval = logic_eval.replace( idx , name_df_ram + "['" + str(idx+markup_sympy) + "']" )
        if name_df_ram+"['"+idx not in logic_eval:
            logic_eval = logic_eval.replace( idx , name_df_ram + "['" + str(idx) + "']" )
        #print(idx)

    #for idx in signal_df.columns:
    #    if not signal_df[idx].any():
    #        del signal_df[idx]
    #        del normalization_methods[idx]#.replace(markup_sympy,'')]
    #        del equations[idx.replace(markup_sympy,'')]

    print(signal_df.tail(1))
    #logic_eval = """{"logic": "(ema-111-@ < ema-22-@)", "equations": {"ema-111": {"equation": "x", "eq_family": "poly"}, "sd-20": {"equation":"-2/cos(x) - 3/cos(x)**4 + 4/sin(x) + 9/sin(x)**4", "eq_family": "periodical"}, "sd-21": {"equation": "-2/cos(x) - 3/cos(x)**4 + 4/sin(x) + 9/sin(x)**4","eq_family": "periodical"}, "sd-111": {"equation": "-2/cos(x) - 3/cos(x)**4 + 4/sin(x) + 9/sin(x)**4","eq_family": "periodical"}, "ema-22": {"equation": "x", "eq_family": "poly"}}, "normalization_methods": {"ema-22-@": "n8", "sd-20-@": "n6", "sd-111-@":"n6", "sd-21-@": "n6", "ema-45-@": "n8"}, "take_profit": {"equation":"(sin(x)/2)**2*100","default":"0.02"}, "stop_loss":{"equation": " sin(x)/4*10","default":"0.02"}, "fitness": "0.968642110351987", "shape_rateo": "0.968642110351987"}"""

    signal = np.array([])
    print(logic_eval)
    signal = eval(logic_eval)

    signal_df = signal_df.iloc[buffer_period:,:]
    
    return signal_df, signal


    
def load_strategy(file_path):
    with open(file_path,'r') as f:
        if len(f.readlines()) != 0:
            f.seek(0)
            lines = f.readlines()
            s = str(lines[0])
            strategy = json.loads(s)
            return strategy
        return None

def compute_max_window_required(strategy):
    params_window_lists = []
    for i in strategy['equations'].keys():
        params_window_lists.append(int(i.split('-')[1]))
    return max(params_window_lists)