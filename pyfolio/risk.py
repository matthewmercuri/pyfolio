import json
import numpy as np

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
        self.beta()

        m = json.dumps(self.metrics, indent=4, sort_keys=False)
        print(m)

    def daily_stats(self):

        # 5 year
        avg_ret = self.returns_df['Percent_Ret'].mean()
        vol = self.returns_df['Percent_Ret'].std()

        # 3 year
        avg_ret_3 = self.returns_df['Percent_Ret'].tail(756).mean()
        vol_3 = self.returns_df['Percent_Ret'].tail(756).std()

        # 1 year
        avg_ret_1 = self.returns_df['Percent_Ret'].tail(252).mean()
        vol_1 = self.returns_df['Percent_Ret'].tail(252).std()

        daily_stats = {'fiveYear': {'meanReturn': avg_ret,
                                    'stdReturn': vol},
                       'threeYear': {'meanReturn': avg_ret_3,
                                     'stdReturn': vol_3},
                       'oneYear': {'meanReturn': avg_ret_1,
                                   'stdReturn': vol_1}}

        self.metrics['dailyStats'] = daily_stats

        return daily_stats

    def beta(self):
        # 5 year daily
        cov_5 = np.cov(self.returns_df['Percent_Ret'],
                       self.returns_df['Bench_P_Ret'])[0][1]
        var_5 = self.returns_df['Bench_P_Ret'].var()

        beta_daily_5 = cov_5 / var_5

        # 3 year daily
        cov_3 = np.cov(self.returns_df['Percent_Ret'].tail(756),
                       self.returns_df['Bench_P_Ret'].tail(756))[0][1]
        var_3 = self.returns_df['Bench_P_Ret'].tail(756).var()

        beta_daily_3 = cov_3 / var_3

        # 3 year daily
        cov_1 = np.cov(self.returns_df['Percent_Ret'].tail(252),
                       self.returns_df['Bench_P_Ret'].tail(252))[0][1]
        var_1 = self.returns_df['Bench_P_Ret'].tail(252).var()

        beta_daily_1 = cov_1 / var_1

        beta = {'fiveYearDaily': beta_daily_5,
                'threeYearDaily': beta_daily_3,
                'oneYearDaily': beta_daily_1}

        self.metrics['beta'] = beta

        return beta
