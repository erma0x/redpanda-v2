from utils.backtest import *
from utils.datasets import load_benchmark
from utils.trading_utils import model_to_signal
import numba

@numba.njit
def max_drawdown(cum_returns):
    max_drawdown = 0.0
    current_max_ret = cum_returns[0]
    for ret in cum_returns:
        if ret > current_max_ret:
            current_max_ret = ret
        max_drawdown = max(max_drawdown, 1 - ret / current_max_ret)
    return max_drawdown

#rolling_1h_max_dd = returns.cumprod().rolling("1h").apply(max_drawdown, raw=True)

def annualised_sharpe(returns, N=252):
    """
    Calculate the annualised Sharpe ratio of a returns stream
    based on a number of trading periods, N. N defaults to 252,
    which then assumes a stream of daily returns.
    The function assumes that the returns are the excess of
    those compared to a benchmark.
    """
    return np.sqrt(N) * returns.mean() / returns.std()

def std_dev(data):
    # Get number of observations
    n = len(data)
    # Calculate mean
    mean = sum(data) / n
    # Calculate deviations from the mean
    deviations = sum([(x - mean)**2 for x in data])
    # Calculate Variance & Standard Deviation
    variance = deviations / (n - 1)
    s = variance**(1/2)
    return s

def sharpe_ratio(data, risk_free_rate=0.0):
    mean_daily_return = sum(data) / len(data)
    sd = std_dev(data)
    daily_sharpe_ratio = (mean_daily_return - risk_free_rate) / sd
    sharpe_ratio = 252**(1/2) * daily_sharpe_ratio
    
    return sharpe_ratio


def covariance(x, y):
    # Finding the mean of the series x and y
    mean_x = sum(x)/float(len(x))
    mean_y = sum(y)/float(len(y))
    # Subtracting mean from the individual elements
    sub_x = [i - mean_x for i in x]
    sub_y = [i - mean_y for i in y]
    numerator = sum([sub_x[i]*sub_y[i] for i in range(len(sub_x))])
    denominator = len(x)-1
    cov = numerator/denominator
    return cov

def correlation(x, y):
    # Finding the mean of the series x and y
    mean_x = sum(x)/float(len(x))
    mean_y = sum(y)/float(len(y))
    # Subtracting mean from the individual elements
    sub_x = [i-mean_x for i in x]
    sub_y = [i-mean_y for i in y]
    # covariance for x and y
    numerator = sum([sub_x[i]*sub_y[i] for i in range(len(sub_x))])
    # Standard Deviation of x and y
    std_deviation_x = sum([sub_x[i]**2.0 for i in range(len(sub_x))])
    std_deviation_y = sum([sub_y[i]**2.0 for i in range(len(sub_y))])
    # squaring by 0.5 to find the square root
    denominator = (std_deviation_x*std_deviation_y)**0.5 # short but equivalent to (std_deviation_x**0.5) * (std_deviation_y**0.5)
    if denominator == 0:
        return 0
    cor = numerator/denominator
    return cor

def compute_SHAPE_RATEO_benchmark():
    df_benchmark = load_benchmark()
    number_of_shares =  initial_amout / df_benchmark['Close'][0]
    benchmark_investment =  number_of_shares * df_benchmark['Close']
    df_benchmark['Daily Return'] = benchmark_investment.pct_change() 
    df_benchmark.dropna(inplace=True)
    shape_rateo_benchmark = sharpe_ratio(df_benchmark['Daily Return'] , risk_free_rate=0.0)
    #print('shape_rateo_benchmark ',shape_rateo_benchmark)
    return shape_rateo_benchmark

def compute_SHAPE_RATEO_trading_strategy(df, strategy):
    #df = load_ETH_USD_2021()
    #strategy = load_strategy('/bot_0_parameters.txt')
    
    df['signal'] = model_to_signal(df = df, model=strategy)
    df['trading strategy'] = backtest( df )
    df['Daily Return'] = df['trading strategy'].pct_change() 
    df.dropna(inplace=True)
    
    shape_rateo_trading_strategy = sharpe_ratio(df['Daily Return'],risk_free_rate=0.00)
    #print('shape_rateo_trading_strategy ',shape_rateo_trading_strategy)
    return shape_rateo_trading_strategy