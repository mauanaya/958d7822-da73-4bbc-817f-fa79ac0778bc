import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Cashflow(object):
   def __init__(self, amount, t):
        self.amount = amount
        self.t = t

   def present_value(self,interest_rate):
        return (self.amount / (1 + self.interest_rate) ** self.t)



class InvestmentProject(object):
    RISK_FREE_RATE = 0.08

    def __init__(self, cashflows, hurdle_rate=RISK_FREE_RATE):
        cashflows_positions = {str(flow.t): flow for flow in cashflows}
        self.cashflow_max_position = max((flow.t for flow in cashflows))
        self.cashflows = []
        for t in range(self.cashflow_max_position + 1):
            self.cashflows.append(cashflows_positions.get(str(t), Cashflow(t=t, amount=0)))
        self.hurdle_rate = hurdle_rate if hurdle_rate else InvestmentProject.RISK_FREE_RATE

    @staticmethod
    def from_csv(filepath, hurdle_rate=RISK_FREE_RATE):
        cashflows = [Cashflow(**row) for row in pd.read_csv(filepath).T.to_dict().values()]
        return InvestmentProject(cashflows=cashflows, hurdle_rate=hurdle_rate)

    @property
    def internal_return_rate(self):
        return np.irr([flow.amount for flow in self.cashflows])

    def get_plot(self, show=False, save=""):
        
            fig = plt.figure(1)
            plot = plt.bar([flow.t for flow in self.cashflows], [flow.amount for flow in self.cashflows])
            plt.xlabel("Time")
            plt.ylabel("Amount")
            plt.title("Cashflows")
            if show:
                plt.show()
            return fig


    def net_present_value(self, interest_rate=None):
        self.interest_rate = interest_rate if interest_rate else self.hurdle_rate
        return np.npv(self.interest_rate,[flow.amount for flow in self.cashflows])

    def equivalent_annuity(self, interest_rate=None):
        return (self.net_present_value(interest_rate=None)*self.interest_rate)/(1-(1+self.interest_rate)**(-self.cashflow_max_position))
        
    def describe(self):
        return {
            "irr": self.internal_return_rate,
            "hurdle-rate": self.hurdle_rate,
            "net-present-value": self.net_present_value(interest_rate=None),
            "equivalent-annuity": self.equivalent_annuity(interest_rate=None)
        }
