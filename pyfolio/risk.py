from . import portfolio


class Risk:

    def __init__(self, portfolio_obj):
        if not isinstance(portfolio_obj, portfolio.Portfolio):
            raise TypeError(f'{portfolio_obj} is not of type: Portfolio')

        self._port = portfolio_obj
        self._port.return_series()

        self.returns_df = self._port.returns_df
        print(self.returns_df)
