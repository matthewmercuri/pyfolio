from . import portfolio

'''
TODO:
- chart growth of 10k
- Fix problem of potentially getting older return series
(maybe just always construct a new return series?)
'''


class Chart:

    def __init__(self, portfolio_obj):
        if not isinstance(portfolio_obj, portfolio.Portfolio):
            raise TypeError(f'{portfolio_obj} is not of type: Portfolio')

        self._port = portfolio_obj

        if self._port.returns_df is None:
            self._port.return_series()

        self.returns_df = self._port.returns_df
        print(self.returns_df)
