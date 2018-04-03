'''
File:
    sample_strategy.py

Description:
    A sample implementation of a portfolio construction strategy
    that would qualify as a submission to the contest.

Questions:
    Please contact jigar@uchicago.edu or vtalasani@uchicago.edu
'''

from portfolio import PortfolioGenerator
import pandas as pd
import numpy as np


class SampleStrategy(PortfolioGenerator):

    def __init__(self):
        pass

    def build_signal(self, stock_features):
        df = stock_features.groupby(
            'timestep', group_keys=False).apply(self.grp)
        time = max(df.index)
        # print(time)
        # print(df.index)
        latest = df[df.index == time].copy()
        # print(latest)
        latest['hml_signal'] = 0
        latest.loc[latest.book_market_ranks == 'growth', 'hml_signal'] = -100
        latest.loc[latest.book_market_ranks == 'value', 'hml_signal'] = 100

        latest['smb_signal'] = 0
        latest.loc[latest.market_cap_ranks == 'small_cap', 'smb_signal'] = -100
        latest.loc[latest.market_cap_ranks == 'big_cap', 'smb_signal'] = 100
        latest = latest.assign(signal=
            (latest.smb_signal + latest.hml_signal)/2, axis=0)
        # print(latest['signal'])
        print(latest)

        return latest.set_index('ticker')['signal']
        # return self.momentum(stock_features)

    def grp(self, data):
        data = data.assign(book_to_market=1 / data.pb)
        dec = pd.qcut(data['book_to_market'], [0, 0.3, 0.7, 1],
                      labels=['growth', 'neutral', 'value'])
        data['book_market_ranks'] = dec

        smb = pd.qcut(data['market_cap'], [0, 0.5, 1],
                      labels=['small_cap', 'big_cap'])
        data['market_cap_ranks'] = smb
        return data

    def momentum(self, stock_features):
        return stock_features.groupby(['ticker'])['returns'].mean()


# Test out performance by running 'python sample_strategy.py'
if __name__ == "__main__":
    portfolio = SampleStrategy()
    sharpe = portfolio.simulate_portfolio()
    print("*** Strategy Sharpe is {} ***".format(sharpe))
