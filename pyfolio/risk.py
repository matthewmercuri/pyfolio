import json

from . import portfolio


class Risk:

    def __init__(self, portfolio_obj):
        if not isinstance(portfolio_obj, portfolio.Portfolio):
            raise TypeError(f'{portfolio_obj} is not of type: Portfolio')

        self._port = portfolio_obj
        self._port.return_series()

        self.returns_df = self._port.returns_df
        self.bench = self._port.bench

        self.metrics = {}

    def all_metrics(self):
        self.daily_stats()

        m = json.dumps(self.metrics, indent=4, sort_keys=False)
        print(m)

    def daily_stats(self):

        # 5 year
        avg_ret = self.returns_df['Percent_Ret'].mean()
        vol = self.returns_df['Percent_Ret'].std()

        self.metrics['dailyStatsFiveYear'] = {'meanDailyReturn': avg_ret,
                                              'stdDailyReturn': vol}

        # 3 year
        avg_ret_3 = self.returns_df['Percent_Ret'].tail(756).mean()
        vol_3 = self.returns_df['Percent_Ret'].tail(756).std()

        self.metrics['dailyStatsThreeYear'] = {'meanDailyReturn': avg_ret_3,
                                               'stdDailyReturn': vol_3}

        # 1 year
        avg_ret_1 = self.returns_df['Percent_Ret'].tail(252).mean()
        vol_1 = self.returns_df['Percent_Ret'].tail(252).std()

        self.metrics['dailyStatsOneYear'] = {'meanDailyReturn': avg_ret_1,
                                             'stdDailyReturn': vol_1}

        return avg_ret, vol

    def beta(self):
        pass
