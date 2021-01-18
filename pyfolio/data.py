from . import yfin


class Data:
    def __init__(self, data_source: str):
        data_source = data_source.upper()
        if data_source not in ['YFINANCE']:
            raise KeyError(f'{data_source} is not a valid data source')
        else:
            self.source = data_source

        self.valid_symbols = self.get_list_valid_symbols()

    def get_list_valid_symbols(self):
        valid_symbols = []

        if self.source == 'YFINANCE':
            valid_symbols = yfin.valid_symbols()

        return valid_symbols

    def validate_symbol(self, symbol: str):
        if self.source != 'YFINANCE':
            if symbol not in self.valid_symbols:
                raise KeyError(f'{symbol} is not a valid symbol')

    def price(self, symbol: str):
        self.validate_symbol(symbol)

        price = 0
        currency = ''
        if self.source == 'YFINANCE':
            price, currency = yfin.price(symbol)

        return price, currency

    def returns(self, symbol: str):
        self.validate_symbol(symbol)

        returns = None
        if self.source == 'YFINANCE':
            returns = yfin.get_returns(symbol)

        return returns

    def fx_df(self):
        returns = None
        if self.source == 'YFINANCE':
            returns = yfin.get_returns('CADUSD=X')
            returns.rename('CAD/USD', inplace=True)

        return returns
