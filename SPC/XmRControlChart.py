"""
An individuals and moving range (X-MR) chart is a pair of control charts for processes
with a subgroup size of one. Used to determine if a process is stable and predictable,
it creates a picture of how the system changes over time. The individual (X) chart displays
individual measurements.

https://sixsigmastudyguide.com/xmr-charts/
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime
from SPC import ControlChart

class XmRControlChart(ControlChart):
    _A2 : float # The Control Chart A2 constant.
    _d2 : float # The Control Chart d2 constant.
    _D3 : float # The Control Chart D3 constant.
    _D4 : float # The Control Chart D4 constant.

    def __init__(self, data:list):
        """ Initialization.

            :param data: values.
        """
        # Initialization of the base class.
        super().__init__(2) # X chart and mR chart.

        # Remember the data.
        self._data = data

        # Remember the Control chart constants size=2 (comparing the current state with previous state).
        self._A2 = 0
        self._d2 = 1.128
        self._D3 = 0
        self._D4 = 3.267

        # The number of samples.
        self.number_of_sample = len(data)

        # Set the values array.
        self.value_X = data

        # Initialize the arrays of X.
        self.cl_X = np.zeros(((self.number_of_sample), 1))
        self.ucl_X = np.zeros(((self.number_of_sample), 1))
        self.lcl_X = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_X = np.zeros(((self.number_of_sample), 1))

        # Initialize the arrays of mR.
        self.value_mR = np.zeros(((self.number_of_sample -1), 1))
        self.cl_mR = np.zeros(((self.number_of_sample -1), 1))
        self.ucl_mR = np.zeros(((self.number_of_sample -1), 1))
        self.lcl_mR = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_plus_mR = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_plus_mR = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_min_mR = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_min_mR = np.zeros(((self.number_of_sample -1), 1))

        # Calculate the difference between the samples.
        for i in range(self.number_of_sample -1):
            self.value_mR[i]=abs(self.value_X[i+1] - self.value_X[i])

        # Calculate the UCL, CL, LCL of X.
        self.cl_X[:] = self.value_X.mean() 
        self.ucl_X[:] = self.value_X.mean() + 3 * self.value_mR.mean() / self._d2
        self.lcl_X[:] = self.value_X.mean() - 3 * self.value_mR.mean() / self._d2

        # Calculate the one and two sigma of X.
        self.two_sigma_plus_X[:] = self.value_X.mean() + 3 * self.value_mR.mean() / self._d2 * 2/3
        self.one_sigma_plus_X[:] = self.value_X.mean() + 3 * self.value_mR.mean() / self._d2 * 1/3
        self.one_sigma_min_X[:] = self.value_X.mean() - 3 * self.value_mR.mean() / self._d2 * 1/3
        self.two_sigma_min_X[:] = self.value_X.mean() - 3 * self.value_mR.mean() / self._d2 * 2/3

        # Calculate the  UCL, CL, LCL of mR.
        self.cl_mR[:] = self.value_mR.mean() 
        self.ucl_mR[:] = self._D4 * self.value_mR.mean()
        self.lcl_mR[:] = self._D3 * self.value_mR.mean()

        # Calculate the one and two sigma of mR.
        self.two_sigma_plus_mR[:] = self.value_mR.mean() + (self._D4 * self.value_mR.mean() - self.value_mR.mean()) * 2/3
        self.one_sigma_plus_mR[:] = self.value_mR.mean() + (self._D4 * self.value_mR.mean() - self.value_mR.mean()) * 1/3
        self.one_sigma_min_mR[:] = self.value_mR.mean() - (self.value_mR.mean() - self._D3 * self.value_mR.mean()) * 1/3
        self.two_sigma_min_mR[:] = self.value_mR.mean() - (self.value_mR.mean() - self._D3 * self.value_mR.mean()) * 2/3

    def plot(self):
        """ Create the plot.
        """
        plt.figure(figsize=(15,10))

        # The 1st vertical plot.
        plt.subplot(2,1,1)

        # The x-axis can be numeric or datetime.
        if (len(super().dates) == 0):
            x_values_X = list(range(0, len(self.value_X)))
        else:
            format=super().dateformat
            x_values_X = [datetime.strptime(d, format).date() for d in super().dates]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(super().dateformat))

        # X chart.
        plt.plot(x_values_X, self.value_X, marker="o", color="k", label="X")
        plt.plot(x_values_X, self.ucl_X, color="r", label="UCL")

        # Retrieve the data.
        df = self.data(0)

        # Plot the signals.
        for i in np.where(df["SIGNAL"])[0]:
            plt.plot(x_values_X[i], self.value_X[i], marker="s", color="r")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_X, self.two_sigma_plus_X, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_X, self.one_sigma_plus_X, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_X, self.cl_X, color="b", label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_X, self.one_sigma_min_X, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_X, self.two_sigma_min_X, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_X, self.lcl_X, color="r", label="LCL")
        plt.title("X Chart")

        # Check numerical or datetime for the x-axis.
        if (len(super().dates) == 0):
            plt.xticks(np.arange(len(self.value_X)))
        else:
            plt.xticks(rotation=45, ha='right')

        # Add a legend.
        plt.legend(loc='upper right')

        # The 2nd vertical plot.
        plt.subplot(2,1,2)

        # The x-axis is numeric.
        x_values_mR = list(range(1, len(self.value_X)))

        # mR chart.
        plt.plot(x_values_mR, self.value_mR, marker="o", color="k", label="R")
        plt.plot(x_values_mR, self.ucl_mR, color="r", label="UCL")

        # Retrieve the data.
        df = self.data(1)

        # Plot the signals.
        for i in np.where(df["SIGNAL"])[0]:
            plt.plot(x_values_mR[i], self.value_mR[i], marker="s", color="r")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_mR, self.two_sigma_plus_mR, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_mR, self.one_sigma_plus_mR, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_mR, self.cl_mR, color="b", label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_mR, self.one_sigma_min_mR, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_mR, self.two_sigma_min_mR, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_mR, self.lcl_mR, color="r", label="LCL")
        plt.title("mR Chart")

        # Set numerical for the x-axis.
        plt.xticks(np.arange(len(self.value_X)))

        # Add a legend.
        plt.legend(loc='upper right')

        # Show the plot.
        plt.show()

    def split(self, stages:list):
        """ Split the chart.

            :param stages: The stages.
        """
        # Include the last index.
        if not self.number_of_sample in stages:
            stages.append(self.number_of_sample)

        # Initialize the arrays of X.
        self.cl_X = np.zeros(((self.number_of_sample), 1))
        self.ucl_X = np.zeros(((self.number_of_sample), 1))
        self.lcl_X = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_X = np.zeros(((self.number_of_sample), 1))

        # Initialize the arrays of mR.
        self.value_mR = np.zeros(((self.number_of_sample -1), 1))
        self.cl_mR = np.zeros(((self.number_of_sample -1), 1))
        self.ucl_mR = np.zeros(((self.number_of_sample -1), 1))
        self.lcl_mR = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_plus_mR = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_plus_mR = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_min_mR = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_min_mR = np.zeros(((self.number_of_sample -1), 1))

        # Calculate the difference between the samples.
        for i in range(self.number_of_sample -1):
            self.value_mR[i]=abs(self.value_X[i+1] - self.value_X[i])

        # Make the calculations on each split, instead of the full data.
        start_index_X = 0
        start_index_mR = 0
        for i in stages:
            # Set the end index.
            end_index_X = i
            end_index_mR = i-1

            # Calculate the UCL, CL, LCL of X.
            self.cl_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() 
            self.ucl_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() + 3 * self.value_mR[start_index_mR:end_index_mR].mean() / self._d2
            self.lcl_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() - 3 * self.value_mR[start_index_mR:end_index_mR].mean() / self._d2

            # Calculate the one and two sigma of X.
            self.two_sigma_plus_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() + 3 * self.value_mR[start_index_mR:end_index_mR].mean() / self._d2 * 2/3
            self.one_sigma_plus_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() + 3 * self.value_mR[start_index_mR:end_index_mR].mean() / self._d2 * 1/3
            self.one_sigma_min_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() - 3 * self.value_mR[start_index_mR:end_index_mR].mean() / self._d2 * 1/3
            self.two_sigma_min_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() - 3 * self.value_mR[start_index_mR:end_index_mR].mean() / self._d2 * 2/3

            # Calculate the  UCL, CL, LCL of mR.
            self.cl_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() 
            self.ucl_mR[start_index_mR:end_index_mR] = self._D4 * self.value_mR[start_index_mR:end_index_mR].mean()
            self.lcl_mR[start_index_mR:end_index_mR] = self._D3 * self.value_mR[start_index_mR:end_index_mR].mean()

            # Calculate the one and two sigma of mR.
            self.two_sigma_plus_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() + (self._D4 * self.value_mR[start_index_mR:end_index_mR].mean() - self.value_mR[start_index_mR:end_index_mR].mean()) * 2/3
            self.one_sigma_plus_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() + (self._D4 * self.value_mR[start_index_mR:end_index_mR].mean() - self.value_mR[start_index_mR:end_index_mR].mean()) * 1/3
            self.one_sigma_min_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() - (self.value_mR[start_index_mR:end_index_mR].mean() - self._D3 * self.value_mR[start_index_mR:end_index_mR].mean()) * 1/3
            self.two_sigma_min_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() - (self.value_mR[start_index_mR:end_index_mR].mean() - self._D3 * self.value_mR[start_index_mR:end_index_mR].mean()) * 2/3

            # Set the start index.
            start_index_X = end_index_X
            start_index_mR = end_index_mR

    def data(self, index:int):
        """ Returns the data.

            :param index: The index for the data (0 = X chart, 1 = mR chart)
        """
        if index == 0: # X chart.
            df = pd.DataFrame(np.column_stack([self.value_X, self.ucl_X, self.two_sigma_plus_X, self.one_sigma_plus_X, self.cl_X, self.one_sigma_min_X, self.two_sigma_min_X, self.lcl_X]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])
            self.execute_rules(df)

            # Check numerical or datetime for the x-axis.
            if (len(super().dates) != 0):
                df['date'] = super().dates
                df=df.set_index('date')

            return df
        if index == 1: # mR chart.
            df = pd.DataFrame(np.column_stack([self.value_mR, self.ucl_mR, self.two_sigma_plus_mR, self.one_sigma_plus_mR, self.cl_mR, self.one_sigma_min_mR, self.two_sigma_min_mR, self.lcl_mR]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])

            self.execute_rules(df)

            return df

        raise ValueError

    def stable(self):
        """ Returns the stable indicator.
        """
        # Execute the rules.
        df = self.data(0)

        if True in df["SIGNAL"].values:
            return False

        # Execute the rules.
        df = self.data(1)

        if True in df["SIGNAL"].values:
            return False

        return True

    def normally_distributed(self, data:list, significance_level:float):
        """ Check if the data follows normal distribution.
            Returns true when the data did not show evidence of non-normality.
            Returns false when the data is not normally distributed.

            :param data: values.
            :param significance_level: significance level.
        """
        return self._normally_distributed(data, significance_level)
