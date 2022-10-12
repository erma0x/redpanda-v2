import random as rnd
import numpy as np
import pandas as pd
import sympy as sym
import pandas_ta as ta

from utils.config import *

def compute_financial_indexes(df, financial_index):
    """
    add new column to df object with the computed financial index
    extract_parameters and call financial indexes equation
    df_indicators can be empty, each call of this function 
    will add a new column with the finance_indicator

       FROM     'sd-60-1' 
       TO       df['sd-60-1']
       
    """
    my_indicator = pd.Series(dtype=float, index=df.index)
    if '-' in financial_index:
        p = financial_index.split('-')

        if 'price' in financial_index:  # SMA
            my_indicator = df['close']

        if 'volume' in financial_index:  # SMA
            my_indicator = df['volume']

        if 'ema' in financial_index:  # SMA
            my_indicator = df.ta.ema(length = int(p[1]))
            
        if 'sd' in financial_index: # SD
            my_indicator = df.ta.stdev(length= int(p[1]))

        if 'roc' in financial_index:
            my_indicator = df.ta.roc(length= int(p[1]))

        if 'rsi' in financial_index:
            my_indicator = df.ta.rsi(length= int(p[1]))

        if 'sma' in financial_index:
            my_indicator = df.ta.sma(length= int(p[1]))

        if 'aberr1' in financial_index:
            my_indicator = df.ta.aberration(int(p[1])).iloc[:, : 1]

        if 'aberr2' in financial_index:
            my_indicator = df.ta.aberration(int(p[1])).iloc[:, 1: 2]

        if 'aberr3' in financial_index:
            my_indicator = df.ta.aberration(int(p[1])).iloc[:, 2: 3]

        if 'aberr3' in financial_index:
            my_indicator = df.ta.aberration(int(p[1])).iloc[:, 3: 4]

        if 'accbands1' in financial_index:
            my_indicator = df.ta.accbands(int(p[1]),p[2],p[3],p[4]).iloc[:, : 1]

        if 'accbands2' in financial_index:
            my_indicator = df.ta.accbands(int(p[1]),p[2],p[3],p[4]).iloc[:, 1: 2]

        if 'accbands3' in financial_index:
            my_indicator = df.ta.accbands(int(p[1]),p[2],p[3],p[4]).iloc[:, 2: 3]

    return my_indicator


def random_indicators(num=5):
    window_lenght = list(range(1,300))
    my_indicators = []

    INDICATORS = available_indicators_dictionary
    for i in range(num):
        indicator = rnd.choice(list(INDICATORS.keys()))
        INDICATOR = ''

        window_lenght = rnd.randint(INDICATORS[indicator]['window']['min'],INDICATORS[indicator]['window']['max'])
        INDICATOR = indicator+'-'+str(window_lenght)

        if len(INDICATORS[indicator].keys())>1:
            for parameter in range(2,len(INDICATORS[indicator].keys())+1):
                if INDICATORS[indicator][str(parameter)]['type']=='float':
                    INDICATOR +='-'+str(round(rnd.uniform(INDICATORS[indicator][str(parameter)]['min'],
                                    INDICATORS[indicator][str(parameter)]['max']),4))

                if INDICATORS[indicator][str(parameter)]['type']=='int':
                    INDICATOR +='-'+ str(rnd.randint(INDICATORS[indicator][str(parameter)]['min'],
                                            INDICATORS[indicator][str(parameter)]['max']))

        
        my_indicators.append(INDICATOR)
    return my_indicators

def math_generator(seed_df, indicators_list):
    '''
    [INPUT] seed_df : pd.DataFrame
    [OUTPUT] math_df : pd.DataFrame
    from technical indicators to subtituted equations arrays
    '''
    math_df = pd.DataFrame()
    equations = dict()

    ## puo andare anche nel ciclo for
    eq_family = rnd.choice( equation_families )
    for indicator in indicators_list:
        equation = check_zero_equation(choose_random_equation(eq_family))
        math_df[indicator+markup_sympy ] = subtitute_expression_to_index(seed_df[indicator],equation)
        equations[indicator]={'equation':equation,'eq_family':eq_family}
    return math_df, equations

def choose_random_equation(equation_family):
    '''
    select random equation from the allowed once
    the input dictionary is available_equations in variables
    '''
    poly = ['polynomial','base']
    periodical = ['fourier','mod_fourier']    
    
    if equation_family=='poly':
        eq_type = rnd.choice(poly)
        if eq_type == 'polynomial':
            return polynomial()
        if eq_type == 'base':
            return base()
    if equation_family=='periodical':
        eq_type = rnd.choice(periodical)
        if eq_type =='fourier':
            return fourier()
        if eq_type=='mod_fourier':
            return mod_fourier()

    else:
        print('ERROR of the function choose_random_equation() Equation Type error')

def check_zero_equation(equation):
    while equation in (0,'0'): 
        key_family = rnd.choice( equation_families )
        equation = choose_random_equation(key_family)
    return equation

def base():
    x = sym.Symbol('x')
    equation = x
    return equation
    
def polynomial():
    indexes_list = rnd.sample(range(min_grade_polynomial,max_grade_polynomial),rnd.choice(range(min_element_ploy,n_elemets_in_equation_poly)))#,``
    parameters_list = [rnd.choice(np.linspace(min_parameter_poly, max_parameter_poly)) for i in range(len(indexes_list))]  # could be 0
    x = sym.Symbol('x')
    equation = sum(k * x ** i for k, i in zip(parameters_list, indexes_list))

    return equation

def fourier():
    indexes_list = rnd.sample(range(min_grade_fourier,max_grade_fourier), rnd.choice(range(n_elemets_in_equation_fourier)))
    list_parameters_1 = np.random.randint(1,10,size=len(indexes_list))
    list_parameters_2 = np.random.randint(1,10,size=len(indexes_list))
    x = sym.Symbol('x')
    equation = sum(k * sym.sin(x) ** i - j * sym.cos(x) ** i for j, k, i in
                        zip(list_parameters_1, list_parameters_2,indexes_list))
    if type(equation) is not int:
        equation = equation.simplify()
    return equation

def mod_fourier():
    indexes_list = rnd.sample(range(min_grade_mod_fourier,max_grade_mod_fourier),rnd.choice(range(n_elemets_in_equation_mod_fourier))) 
    list_parameters_1 = np.random.randint(1,10,size=len(indexes_list)) # min, max, size
    list_parameters_2 = np.random.randint(1,10,size=len(indexes_list))
    x = sym.Symbol('x')
    equation = sum(k * sym.sin(x) ** i - j * sym.cos(x) ** i for j, k, i in
                        zip(list_parameters_1, list_parameters_2,indexes_list))
    if type(equation) is not int :
        equation = equation.simplify()                    
    return equation

def subtitute_expression_to_index(my_array,equation): 
    """
    Apply the equation to the array   
    [IN] x: sympy symbol, x can be also be  (x,y,z,k)
         equation: str or sympy equation
    [OUT] signal_data: np.bool()
    """
    f = sym.lambdify(x, equation,"numpy")     
    signal_data = f(my_array)            
    return(signal_data)

##################################################################################################################################################
                        # NORMALIZATION

def apply_normalization(nparray,method='n1'):
    """
    apply the normalization method to the array of numbers
    must be applied to arrays and not direct to equation
    """
    n_type = method
    if n_type=='n0':
        return n0(nparray)
    if n_type=='n1':
        return n1(nparray)
    elif n_type=='n2':
        return n2(nparray)
    elif n_type=='n3':
        return n3(nparray)
    elif n_type=='n4':
        return n4(nparray)
    elif n_type=='n5':
        return n5(nparray)
    elif n_type=='n6':
        return n6(nparray)
    elif n_type=='n7':
        return n7(nparray)  
    elif n_type=='n8':
        return n8(nparray)  
    elif n_type=='n9':
        return n9(nparray)  
    elif n_type=='n10':
        return n10(nparray)  
    elif n_type=='n11':
        return n11(nparray)  
    elif n_type=='n12':
        return n12(nparray)  
    elif n_type=='n13':
        return n13(nparray)  
    elif n_type=='n14':
        return n14(nparray)  
    elif n_type=='n15':
        return n15(nparray)  
    elif n_type=='n16':
        return n16(nparray)  
    elif n_type=='n17':
        return n17(nparray)  
    else:
        print(' normalization type error')

def n0(nparray):
    # between 0 and 1
    return (nparray - np.min(nparray))/np.ptp(nparray)

#@jit(nopython=True)
def n1(nparray):
    """ ( array - Min) / (Max - Min) """
    return (nparray - np.min(nparray)) / (np.max(nparray) - np.min(nparray))
    
#@jit(nopython=True)
def n2(nparray):
    """(array - mean) / sd """
    return (nparray - np.mean(nparray) ) / np.std(nparray)

#@jit(nopython=True)
def n3(nparray):
    """(array - mean) / var """
    return (nparray - np.mean(nparray) ) / np.var(nparray)

#@jit(nopython=True)
def n4(nparray):
    """(array - mean) / (Max - min) """
    return (nparray - np.mean(nparray)) / (np.max(nparray) - np.min(nparray))

#@jit(nopython=True)
def n5(nparray):
    """ 1 / (1 + e^(-i)) """
    e = 2.71828
    return 1 / (1 + e**(-nparray))

#@jit(nopython=True)
def n6(nparray):
    return np.log10(np.absolute(nparray)) / (1 - np.log10(np.absolute(nparray)))

#@jit(nopython=True)
def n7(nparray):
    e = 2.71828
    var = nparray.var()
    return nparray**e / (1+var)

#@jit(nopython=True)
def n8(nparray):
    return np.sin(np.absolute(nparray)) / ( np.cos(np.absolute(nparray)))

#@jit(nopython=True)
def n9(nparray):
    return ((np.tanh(nparray) - np.tan(nparray)) + np.max(nparray) ) / (np.max(nparray)) 

def n10(nparray):
    return np.sin(nparray)**2  - np.tan(nparray)**2  

def n11(nparray):
    return np.cos(nparray)**2  - np.tan(nparray)**2  

def n12(nparray):
    return np.sin(nparray)**2  - np.tanh(nparray)**2  
        
def n13(nparray):
    return np.cos(nparray)**2  - np.tanh(nparray)**2 

def n14(nparray):
    return np.cos(nparray) - np.tanh(nparray) / max(np.tanh(nparray)) 

def n15(nparray):
    return np.cos(nparray) - np.tanh(nparray) / (np.cos(nparray) + np.cos(nparray) )

def n16(nparray):
    return (np.sin(nparray)-np.cumsum(nparray)**2)

def n17(nparray):
    e = 2.718281828459045
    return (np.cos(nparray) + np.sin(nparray))/e

##################################################################################################################################################
                        # LOGIC

def extract_logic_string(logic):
    return logic.replace("final_df['"," ").replace("'].all()"," ")

def random_name(names):
    name=''
    for i in range(1):
        name+=rnd.choice(names)
    return name

def R(number_choice=2):
    return(rnd.randrange(0,number_choice))

def generate_logic_rules(dataframe_name='df',names=['🐶','🐒','🦍','🐺','🦝','🦊','🦁','🐯']):    
    """ GENERATE LOGIC WITH COMPARISON OF SIMILAR INDEXES
    """
    operation_trading_rule= ''

    index_number = rnd.randrange(min_index_number_allowed, max_index_number_allowed)
    while operation_trading_rule in not_valid_eq:
        for i in range(index_number):
            operation_trading_rule=''
            flag_external=False
            number_of_disequations = rnd.choice(range(numer_of_disequations))
            for j in range(number_of_disequations):
                
                logic_operator = '' # (Q<N)
                idx1= random_name(names)
                idx2= random_name(names)

                if flag_external==True: # CLOSE EXTERNAL BRACKET
                    if j==number_of_disequations-2:
                        operation_trading_rule+=' ) '
                    if rnd.random()>.8:
                        operation_trading_rule+=' ) '
                        flag_external=False
                        x=0

                if j>0 and j<numer_of_disequations : # ADD LOGIC: AND, OR
                    operation_trading_rule+=rnd.choice(and_or) 

                if flag_external==False and j<numer_of_disequations-2 and rnd.random()>.8:
                    #operation_trading_rule+=' ( '
                    flag_external=True
                    x=j
                
                logic_operator = " ( "+dataframe_name+"['"+idx1+"']  " +major_minor[R()]+" "+dataframe_name+"['"+idx2+"'] ) "
                operation_trading_rule+=logic_operator
                

    diff = int(operation_trading_rule.count(')'))-int(operation_trading_rule.count('('))
    if diff<0:
        operation_trading_rule = operation_trading_rule+')'*diff
    elif diff>0:
        operation_trading_rule = '('*diff+operation_trading_rule
    else:
        pass
    
    return operation_trading_rule