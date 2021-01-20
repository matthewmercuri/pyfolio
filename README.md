# pyfolio
A python library that helps assess one's investment portfolio risk.

---

### This is currently a work in progress (as I'm sure all projects are 😅)!
Below you will find the features and capabilities as I implement them.

### TODO 📝
Note: only items that are completely implemented are marked complete. If an item is not checked off, it may be only partly implemented.
- [ ] Portfolio Object 📁
  - [x] add or remove equity and cash positions
  - [x] create a pandas dataframe that calculates daily returns from positions
  - [x] handle Canadian and American symbols (FX conversion)
  - [x] print portfolio as a JSON object
  - [x] calculate daily portfolio value, percent return, log return
  - [x] create a pandas df containing daily price data for holdings, total value, and benchmark
  - [x] save and load user's portfolios
- [ ] Data Object 📊
  - [x] get daily returns for symbols
  - [x] get latest price for symbols
  - [x] get CAD/USD FX data
  - [x] data source agnostic
  - [ ] client-side symbol validation
  - [ ] Data Sources
    - [x] yfinance
    - [ ] tiingo?
    - [ ] IEX?
    - [ ] use env variables to configure APIs
- [ ] Risk Object 📉📈
  - [x] accept portfolio object in class constructor
  - [x] daily average return and volatitily (standard deviation)
  - [x] Daily Beta
  - [ ] Sharpe Ratio
  - [ ] Correlation Matrix
  - [ ] Value at Risk (VaR)
    - [ ] historical (1, 3, 5 years)
    - [ ] student's t
    - [ ] monte carlo?
  - [ ] Expected Shortfall (ES/cVaR)
    - [ ] historical (1, 3, 5 years)
    - [ ] student's t
    - [ ] monte carlo?
