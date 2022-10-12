import pandas as pd
from utils.datasets import load_ETHUSD_2021
from utils.trading_utils import *
from utils.config import *
from utils.backtest import *
from utils.datasets import *

df = load_ETHUSD_2021()
trading_strategy = load_strategy(MODEL_PATH_daemon_hunter)
backtest( df , trading_strategy , print_operations = True, equity = 100_000 )
