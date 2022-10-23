import itertools
import math
import numpy as np

stocks_count = 3

# Order of data is AAPL, GOOG, AMZN
risk_free_daily_interest_rate = 0.00016
mean_returns = [0.044857944, 0.029035134, 0.010361979]
std_dev = [0.009320453, 0.00837577, 0.009556763]
correlation = [
    [0, 0.698431255, 0.660738586], 
    [0.698431255, 0, 0.679322691], 
    [0.660738586, 0.679322691, 0]
]


def get_portfolio_std_dev(weights):

    portfolio_variance = 0

    for i in range(stocks_count):
        portfolio_variance = portfolio_variance + weights[i] * weights[i] * std_dev[i] * std_dev[i]

    for pair in itertools.product(list(range(0 , stocks_count)), repeat=2):
        if pair[0] < pair[1]:
            i = pair[0]
            j = pair[1]
            portfolio_variance = portfolio_variance + 2 * correlation[i][j] * weights[i] * weights[j] * std_dev[i] * std_dev[j]

    return math.sqrt(portfolio_variance)


def get_portfolio_returns(weights):
    portfolio_returns = 0

    for i in range(stocks_count):
        portfolio_returns = portfolio_returns + weights[i] * mean_returns[i]

    return portfolio_returns


if __name__ == "__main__":

    max_sharpe_ratio = -100
    optimal_weights = []
    max_returns = 0
    best_std_dev = 0
    for w1 in np.arange(0, 1.005, 0.01):
        for w2 in np.arange(0, 1.005, 0.01):
            for w3 in np.arange(0, 1.005, 0.01):
                if w1 + w2 + w3 == 1:
                    weights = [w1, w2, w3]
                    returns = get_portfolio_returns(weights) - risk_free_daily_interest_rate
                    portfolio_std_dev = get_portfolio_std_dev(weights)
                    sharpe_ratio = returns / portfolio_std_dev
                    if sharpe_ratio > max_sharpe_ratio:
                        max_sharpe_ratio = sharpe_ratio
                        best_returns = returns + risk_free_daily_interest_rate
                        best_std_dev = portfolio_std_dev
                        optimal_weights = weights

    print("max_sharpe_ratio: ", max_sharpe_ratio)
    print("optimal_weights: ", optimal_weights)
    print("returns (in percent): ", best_returns*100)
    print("std_dev (in percent): ", best_std_dev*100)

    # RESULTS:
    # max_sharpe_ratio:  4.79762413318264
    # optimal_weights:  [0.96, 0.04, 0.0]
    # returns (in percent):  4.406503159999999
    # std_dev (in percent):  0.9184761118576458  

