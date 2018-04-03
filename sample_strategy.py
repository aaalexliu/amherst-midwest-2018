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
        time = max(stock_features.index)

        umd = self.month_momentum(stock_features)
        latest = stock_features[stock_features.index == time].copy()

        latest = latest.merge(umd, how = 'left', on = 'ticker')
        latest['umd_signal'] = 0
        latest.loc[latest.momentum_rank == 'highest', 'umd_signal'] = 100
        latest.loc[latest.momentum_rank == 'lowest', 'umd_signal'] = -100
        # print(latest)
        # latest = latest.groupby(
        #     'timestep', group_keys=False).apply(self.grp)
        # # print(time)
        # # print(df.index)
        # # print(latest)
        # latest['hml_signal'] = 0
        # latest.loc[latest.book_market_ranks == 'growth', 'hml_signal'] = -100
        # latest.loc[latest.book_market_ranks == 'value', 'hml_signal'] = 100

        # latest['smb_signal'] = 0
        # latest.loc[latest.market_cap_ranks == 'small_cap', 'smb_signal'] = -20
        # latest.loc[latest.market_cap_ranks == 'big_cap', 'smb_signal'] = 20
        latest = latest.assign(signal = latest.umd_signal)
        # signal=(latest.smb_signal + latest.hml_signal) / 2)
        # print(latest['signal'])
        # print(latest)

        return latest.set_index('ticker')['signal']
        # return self.momentum(stock_features)

    def month_momentum(self, data):
        result = pd.DataFrame(columns=['ticker', 'momentum'])

        for x in range(0, 1000):
            ticker_df = data[data.ticker == x]
        #     ticker_df['momentum'] = ticker_df.pivot_table(index='timestep', values='returns', aggfunc=lambda x: np.cumprod(1 + x.tail(50).head(30)).tail(1))
        #     print(ticker_df.returns)
        #     display(ticker_df)
            cum = ticker_df.returns + 1
        #     print('just plus one')
        #     display(cum[1:20])
            total = np.cumprod(cum[0:30]) * 100
            # print(len(total))
            # print(total.iloc[29])
            # display(total[20:29])
        #     print(total.colnames())
        #     print('michael momentum')
        #     display(ticker_df.momentum[1:20])
            # print(total.iloc[29])
            result = result.append({'ticker': x, 'momentum': total.iloc[29]},
                                   ignore_index=True)
        result['rank'] = result['momentum'].rank(method='first')
        dec = pd.qcut(result['rank'], [0, 0.3, 0.7, 1], labels=[
                      'lowest', 'middle', 'highest'], duplicates='drop')
        result['momentum_rank'] = dec
        print(result)
        return result

    def grp(self, data):
        data = data.assign(book_to_market=1 / data.pb)
        dec = pd.qcut(data['book_to_market'], [0, 0.3, 0.7, 1],
                      labels=['growth', 'neutral', 'value'])
        data['book_market_ranks'] = dec

        smb = pd.qcut(data['market_cap'], [0, 0.1, 0.9, 1],
                      labels=['small_cap', 'middle', 'big_cap'])
        data['market_cap_ranks'] = smb
        return data

    def momentum(self, stock_features):
        return stock_features.groupby(['ticker'])['returns'].mean()


# Test out performance by running 'python sample_strategy.py'
if __name__ == "__main__":
    portfolio = SampleStrategy()
    sharpe = portfolio.simulate_portfolio()
    print("*** Strategy Sharpe is {} ***".format(sharpe))
