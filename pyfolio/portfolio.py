import json
import numpy as np
import pandas as pd

from . import data


class Portfolio:

    def __init__(self, bench: str = 'sp500', data_source: str = 'yfinance'):
        # perhaps I should store this in env variables
        self._data_source = data_source
        self.bench = self._validate_bench(bench)
        self.MIN_DATES = 1260

        self.returns_df = None
        self.returns = None

        self.portfolio = {}
        self.portfolio['Cash'] = {'USD': 0, 'CAD': 0}

        self.portfolio['Holdings'] = {}

        self.data = data.Data(data_source)
        self.fx_df = self.data.fx_df()

    def _validate_bench(self, bench):
        bench = bench.upper()
        if bench not in ['SP500']:
            raise KeyError(f'{bench} is not a valid benchmark!')

        return bench

    def _add_benchmark(self, ret_df):
        # time.sleep?
        bench_df = self.data.bench(self.bench)
        returns_df = pd.concat([ret_df, bench_df], axis=1)
        returns_df['Bench_P_Ret'] = returns_df['Bench'].pct_change(periods=1)

        return returns_df

    def add_cash(self, amount: float, currency: str):
        currency = currency.upper()

        if currency not in ['USD', 'CAD']:
            raise KeyError(f'{currency} is not a valid currency')

        if currency == 'USD':
            self.portfolio['Cash']['USD'] += amount
        elif currency == 'CAD':
            self.portfolio['Cash']['CAD'] += amount
        else:
            print('Issue with adding cash to portfolio.')

    def add_position(self, symbol: str, shares: int):
        symbol = symbol.upper()

        price, currency = self.data.price(symbol)
        total_value = round(price*shares, 2)

        self.portfolio['Holdings'][symbol] = {'shares': shares,
                                              'share_price': price,
                                              'total_value': total_value,
                                              'currency': currency}

    def remove_position(self, symbol: str):
        del self.portfolio['Holdings'][symbol]

    def positions(self):
        positions_dict = self.portfolio['Holdings']
        positions = list(positions_dict.keys())

        return positions

    def return_series(self):
        positions = self.positions()
        min_dates = self.MIN_DATES
        ticker_returns_dfs = []

        for pos in positions:
            # may need to add a time.sleep here
            ticker_return_df = self.data.returns(pos)
            shares = self.portfolio['Holdings'][pos]['shares']
            if len(ticker_return_df) < min_dates:
                min_dates = len(ticker_return_df)

            ticker_return_df = ticker_return_df * shares

            # Convert to USD if ticker is CAD
            if self.portfolio['Holdings'][pos]['currency'] == 'CAD':
                temp_df = pd.concat([ticker_return_df, self.fx_df], axis=1)
                temp_df.dropna(inplace=True)
                temp_df[pos] = temp_df[temp_df.columns[0]]*temp_df['CAD/USD']
                ticker_return_df = temp_df[pos]

            ticker_returns_dfs.append(ticker_return_df)

        returns_df = pd.concat(ticker_returns_dfs, axis=1)
        returns_df.columns = positions

        # Forward fill for days the US trades and Can doesn't (or vice versa)
        returns_df.fillna(method='ffill', inplace=True)

        returns_df['TOTAL'] = returns_df[list(returns_df.columns)].sum(axis=1)

        returns_df['Percent_Ret'] = returns_df['TOTAL'].pct_change(periods=1)
        # returns_df['Percent_Ret'] = returns_df['Percent_Ret']*100

        returns_df['Log_Ret'] = (np.log(returns_df['TOTAL'])
                                 - np.log(returns_df['TOTAL'].shift(1)))
        # returns_df['Log_Ret'] = returns_df['Log_Ret']*100

        # Adding benchmark pricing data
        returns_df = self._add_benchmark(returns_df)

        returns_df = returns_df.tail(self.MIN_DATES)

        self.returns_df = returns_df
        self.returns = returns_df['TOTAL']

        if min_dates < self.MIN_DATES:
            print('WARNING: This portfolio does not have 5 years of data!')

        return returns_df

    def show(self):
        p = json.dumps(self.portfolio, indent=4, sort_keys=True)
        print(p)
