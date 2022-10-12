import sys
import numpy as np
import sympy as sym

ROOT_PATH = sys.path[0].replace('/utils','')
MODEL_PATH_daemon_hunter = ROOT_PATH + '/models/daemon_hunter.txt'
DATA_FILE_NAME_BENCHMARK = ROOT_PATH + '/data/snp500_2021.csv'
DATA_FILE_NAME_EURUSD_1m_2022 =  ROOT_PATH + '/data/EUR_USD_1m_test_4.csv'
DATA_FILE_NAME_SIGNAL =  ROOT_PATH + '/data/EUR_USD_1m_test_4_signal.csv'
DATA_FILE_NAME_ETHUSD_1m_2021 =  ROOT_PATH + '/data/ETH_USD_1m_2021.csv'

POP_SIZE = 100
GENERATIONS = 10

MUTATION_RATE = 0.05
CROSS_OVER_RATE = 0.5
SELECTION_FITNESS_FIRST_GEN = 0.2
SELECTION_FINTESS  = 3.0

initial_amout = 100_000
print_operations = True
gabmling_space = np.linspace(0.0005,0.1,1000)

take_profit = 0.005
stop_loss = 0.01
n_element = 0 
name_df_ram = 'signal_df'
n_points_plot = 400

global experiment_number
experiment_number = 0 

global number_of_plots
number_of_plots = 0

markup_sympy = '-@'
buffer_period = 400

x = sym.Symbol('x')

min_index_number_allowed = 2
max_index_number_allowed = 5
numer_of_disequations = 3
and_or = ['and' , 'or']
math_symbols = ['/' , '*' , '+' , '-' , '**' , 'log' , 'ln']
major_minor = ['>' , '<']
br_open = ['(' , '']
br_close = [')' , '']
not_valid_eq = (' ','','(( )','( ))','(())','()')


# polynomial
max_grade_polynomial = 10         # max grade of the polinomial
min_grade_polynomial = -10
n_elemets_in_equation_poly = 3    # max number of elements allowed in the same function
min_element_ploy = 1
min_parameter_poly = -1           # min of the parameters of the equation
max_parameter_poly = 1            # max of the parameters of the equation
	
# fourier
max_grade_fourier = 10           # max grade of the fourier
min_grade_fourier = -10
n_elemets_in_equation_fourier = 3   
min_parameter_fourier = -1
max_parameter_fourier = 1

# modded fourier
max_grade_mod_fourier = 10
min_grade_mod_fourier = -10
n_elemets_in_equation_mod_fourier = 3
min_parameter_mod_fourier = -1
max_parameter_mod_fourier = 1

available_indicators = ['smi','ema','roc','sd','price','volume',
'aberration_1','aberration_2','aberration_3',
'accbands_1','accbands_2','accbands_3','accbands_4']

available_indicators_dictionary = {'smi':{'window':{'max':100,'min':2,'type':'int'}},

                                   'sma':{'window':{'max':10,'min':2,'type':'int'}},

                                    'ema':{'window':{'max':100,'min':2,'type':'int'}},

                                    #'wma':{'window':{'max':10,'min':2,'type':'int'}},

                                    'rsi':{'window':{'max':100,'min':2,'type':'int'}},
                                    
									'sd':{'window':{'max':100,'min':2,'type':'int'}},

                                    # 'accbands_1':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'},
                                    #         '4':{'max':100,'min':0.01,'type':'float'}
									# },
                                    # 'accbands_2':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'},
                                    #         '4':{'max':100,'min':0.01,'type':'float'}
									# },
                                    # 'accbands_3':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'},
                                    #         '4':{'max':100,'min':0.01,'type':'float'}
									# },
                                    # 'accbands_4':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'},
                                    #         '4':{'max':100,'min':0.01,'type':'float'}
									# },
                                    # 'aberration_1':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'}},
                                    # 'aberration_2':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'}},
                                    # 'aberration_3':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'}},

                                    # 'ad':{'window':{'max':10,'min':2,'type':'int'},
                                    #         '2':{'max':100,'min':0.01,'type':'float'},
                                    #         '3':{'max':100,'min':0.01,'type':'float'}},

                                    # 'adosc':{'window':{'max':10000,'min':2,'type':'int'},
                                    #         '2':{'max':10000,'min':1.0,'type':'float'},
                                    #         '3':{'max':10000,'min':0.01,'type':'float'},
                                    #         '4':{'max':10000,'min':0.01,'type':'float'}}
								}											

available_normalizations=['n1','n2','n3','n4']#,'n5','n6','n7','n8','n9','n10','n11','n12','n13','n14','n15','n16','n17']
equation_families = ('poly','periodical')

max_parameter_2_accbands = 100
max_parameter_3_accbands = 100
max_parameter_4_accbands = 100

base_operation_data_structure = {'side':'',
								'symbol':'',
								'take_profits':[],
								'entry_prices':[],
								'stop_losses':[],
								'laverage':10}

model_base_data_structure =  {
			'fitness':0.0,
			'mutated':False,
			'name':'unknown',
			'ticker':'',
			'leverage':0,
			'logic':'',
			'equations':{},
			'normalization_methods':{},
			'performance':{}
			}
			
#TEST_STRATEGY = {"logic": "(sd-3-@  >  sd-21-@ )" ,"equations": {"sma-29": {"equation": "x", "eq_family": "poly"}, "sd-3": {"equation":"-2/cos(x) - 3/cos(x)**4 + 4/sin(x) + 9/sin(x)**4", "eq_family": "periodical"}, "sd-21": {"equation": "x", "eq_family": "poly"}, "roc-35": {"equation": "x", "eq_family": "poly"}, "sma-13": {"equation": "x", "eq_family": "poly"}}, "normalization_methods": {"sma-29-@": "n2", "sd-3-@": "n7", "sd-21-@": "n6", "roc-35-@": "n1", "sma-13-@": "n2"}, "take_profit": "0.02424174174174174", "stop_loss": "0.020284784784784782", "fitness": "0.968642110351987", "shape_rateo": "0.968642110351987"}

# {'side': 'buy',
#  'symbol': 'ETH-PERP',
#  'take_profits': ['3400', '3300','3200'],
#  'entry_prices': ['2900', '3000'], 
# 'stop_losses': ['2000','1900'],
# 'laverage': 10}
