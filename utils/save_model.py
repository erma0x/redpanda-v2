import os
from utils.config import *

def save_parameters(input_text:str='Test'):
    if type(input_text) != str:
        input_text = str(input_text)    

    if not os.path.exists(ROOT_PATH +'/runs/experiment_' + str(experiment_number)):
        os.makedirs(ROOT_PATH +'/runs/experiment_' + str(experiment_number))
        f = open(ROOT_PATH +'/runs/experiment_' + str(experiment_number) + f"/bot_{number_of_plots}_parameters.txt" , "x")
        f.write(input_text)
    
    else:
        f = open(ROOT_PATH +'/runs/experiment_' + str(experiment_number) + f"/bot_{number_of_plots}_parameters.txt" , "w")
        f.write(input_text)

    f.close()
