"""
The abstract class for a control chart.
"""

import pandas as pd
import ruptures as rpt
import warnings
from SPC import Rule
from abc import ABC, abstractmethod
from kneed import KneeLocator
from scipy.stats import jarque_bera
from scipy.stats import shapiro
warnings.filterwarnings("ignore")

class ControlChart(ABC):
    _limits = False # The limits indicator for +2s, +1s, -1s, -2s.
    _dateformat = "%Y-%m-%d" # The date format.
    _dates = [] # The dates.
    _rules = list() # The rules.

    def __init__(self, number_of_charts : int):
        """ Initialization.

            :param number_of_charts: The number of charts.
        """
        # The number of charts.
        self._number_of_charts = number_of_charts

    @abstractmethod
    def plot(self):
        """ Plot the chart(s).
        """
        pass

    @abstractmethod
    def split(self, stages:list):
        """ Split the chart.

            :param stages: The stages.
        """
        pass

    @abstractmethod
    def data(self, index:int):
        """ Returns the data.

            :param index: The index for the data.
        """
        pass

    @property
    def limits(self):
        """ Returns the limits indicator.
        """
        return self._limits

    @limits.setter
    def limits(self, limits):
        """ Set the limits indicator.

            :param limits: The limits indicator.
        """
        self._limits = limits

    @property
    def number_of_charts(self):
        """ Returns the number of charts.
        """
        return self._number_of_charts

    @property
    def dates(self):
        """ Returns the dates.
        """
        return self._dates
	
    @dates.setter
    def dates(self, dates:list):
        """ Set the dates for the x-axis.

            :param dates: The dates.
        """
        self._dates = dates

    @property
    def dateformat(self) -> str:
        """ Returns the date format.
        """
        return self._dateformat
	
    @dateformat.setter
    def dateformat(self, dateformat:str):
        """ Sets the date format.

            :param dateformat: The date format.
        """
        self._dateformat = dateformat

    @abstractmethod
    def stable(self):
        """ Returns the stable indicator.
        """
        pass

    def append_rule(self, rule : Rule):
        """ Append a rule.

            :param rule: The rule.
        """
        # Append the rule.
        self._rules.append(rule)

    def execute_rules(self, df: pd.DataFrame):
        """ Rules execution.

            :param df: The dataframe.
        """
        # Create the signal column.
        df["SIGNAL"] = False

        for rule in self._rules:
            rule.execute(df)

    def stages(self, data:list, max_stages:int):
        """ Plot the chart(s).

            :param data: values.
            :param max_stages: the maximum possible of stages.
        """
        # Determining errors for possible number of stages.
        sum_errors = []
        for i in range (1, max_stages):
            model = rpt.Dynp(model="l2") # L2=Euclidean Distance.
            model.fit(data)
            stages = model.predict(n_bkps=i-1)
            error=model.cost.sum_of_costs(stages)
            sum_errors.append(error)

        # Calculate optimal number of stages.
        x = range(1, len(sum_errors)+1)
        kn = KneeLocator(x, sum_errors, curve='convex', direction='decreasing')

        # Determine the indexes of the optimal number of stages.
        if kn.knee is not None:
            stages = model.predict(n_bkps=kn.knee)
            return stages
        else:
            return None

    def _normally_distributed(self, data:list, significance_level:float):
        """ Check if the data follows normal distribution.
            Returns true when the data did not show evidence of non-normality.
            Returns false when the data is not normally distributed.

            :param data: values.
            :param significance_level: significance level.
        """
        if (len(data) > 5000):
            stat,p = jarque_bera(data)
        else:
            stat,p = shapiro(data)

        if p > significance_level:
            return True
        else:
            return False
