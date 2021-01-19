from pyfolio import portfolio
from pyfolio import charts
from pyfolio import risk

Portfolio = portfolio.Portfolio()
# Portfolio.add_cash(1000, 'usd')
Portfolio.add_position('AAPL', 2)
# Portfolio.add_position('AMD', 2)
# Portfolio.add_position('TD.to', 2)
# print(Portfolio.positions())
# Portfolio.remove_position('AAPL')
# Portfolio.show()
# print(Portfolio.return_series())
# charts.Chart(Portfolio)

# print(Portfolio.return_series())

Risk = risk.Risk(Portfolio)
Risk.all_metrics()
