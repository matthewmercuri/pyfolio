import yfinance as yf


def valid_symbols():
    return []


def price(symbol):
    _ticker = yf.Ticker(symbol)
    _returns = _ticker.history(period='max')
    price = _returns['Close'].tail(1).iloc[0]
    price = round(price, 4)

    currency = _ticker.info['currency']

    return price, currency


def get_returns(symbol):
    _ticker = yf.Ticker(symbol)
    _returns = _ticker.history(period='max')
    returns = _returns['Close']

    return returns
