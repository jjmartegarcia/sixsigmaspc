"""
The x-bar and R-chart are control charts used to monitor the mean and variation of a
process based on samples taken in a given time.

X-bar chart: The mean or average change in process over time from subgroup values.
The control limits on the X-Bar brings the sample’s mean and center into consideration.

R-chart: The range of the process over the time from subgroups values.
This monitors the spread of the process over the time.

https://sixsigmastudyguide.com/x-bar-r-control-charts/
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime
from SPC import ControlChart
from SPC import XbarRControlChartConstants

class XbarRControlChart(ControlChart):
    _A2 : float # The Control Chart A2 constant.
    _d2 : float # The Control Chart d2 constant.
    _D3 : float # The Control Chart D3 constant.
    _D4 : float # The Control Chart D4 constant.

    def __init__(self, data:list):
        """ Initialization.

            :param data: values.
        """
        # Initialization of the base class.
        super().__init__(2) # X bar chart and R chart.

        # Remember the data.
        self._data = data

        # Initialization of the constants.
        constants = XbarRControlChartConstants()

        # Determine the subgroup size.
        n = len(data[0])

        # Remember the Control chart constants.
        self._A2 = constants.get_constant(n, 0)
        self._d2 = constants.get_constant(n, 1)
        self._D3 = constants.get_constant(n, 2)
        self._D4 = constants.get_constant(n, 3)

        # The number of samples.
        self.number_of_sample = len(data)

        # Initialize the arrays of X bar.
        self.value_X = np.zeros(((self.number_of_sample), 1))
        self.cl_Xbar = np.zeros(((self.number_of_sample), 1))
        self.ucl_Xbar = np.zeros(((self.number_of_sample), 1))
        self.lcl_Xbar = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_X = np.zeros(((self.number_of_sample), 1))

        # Initialize the arrays of R.
        self.value_R = np.zeros(((self.number_of_sample), 1))
        self.cl_R = np.zeros(((self.number_of_sample), 1))
        self.ucl_R = np.zeros(((self.number_of_sample), 1))
        self.lcl_R = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_R = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_R = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_R = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_R = np.zeros(((self.number_of_sample), 1))

        # Set the values for X bar and R.
        for i in range(self.number_of_sample):
            self.value_X[i] = data[i].mean()
            self.value_R[i] = data[i].max() - data[i].min()

        # Calculate the UCL, CL, LCL of X bar.
        self.cl_Xbar[:] = self.value_X.mean() 
        self.ucl_Xbar[:] = self.value_X.mean() + self._A2 * self.value_R.mean()
        self.lcl_Xbar[:] = self.value_X.mean() - self._A2 * self.value_R.mean()

        # Calculate the one and two sigma of X bar.
        self.two_sigma_plus_X[:] = self.value_X.mean() + self._A2 * self.value_R.mean() * 2/3
        self.one_sigma_plus_X[:] = self.value_X.mean() + self._A2 * self.value_R.mean() * 1/3
        self.one_sigma_min_X[:] = self.value_X.mean() - self._A2 * self.value_R.mean() * 1/3
        self.two_sigma_min_X[:] = self.value_X.mean() - self._A2 * self.value_R.mean() * 2/3

        # Calculate the  UCL, CL, LCL of R.
        self.cl_R[:] = self.value_R.mean() 
        self.ucl_R[:] = self._D4 * self.value_R.mean()
        self.lcl_R[:] = self._D3 * self.value_R.mean()

        # Calculate the one and two sigma of R.
        self.two_sigma_plus_R[:] = self.value_R.mean() + (self._D4 * self.value_R.mean() - self.value_R.mean()) * 2/3
        self.one_sigma_plus_R[:] = self.value_R.mean() + (self._D4 * self.value_R.mean() - self.value_R.mean()) * 1/3
        self.one_sigma_min_R[:] = self.value_R.mean() - (self.value_R.mean() - self._D3 * self.value_R.mean()) * 1/3
        self.two_sigma_min_R[:] = self.value_R.mean() - (self.value_R.mean() - self._D3 * self.value_R.mean()) * 2/3

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

        # X bar chart.
        plt.plot(x_values_X, self.value_X, marker="o", color="k", label="X bar")
        plt.plot(x_values_X, self.ucl_Xbar, color="r", label="UCL")

        # Retrieve the data.
        df = self.data(0)

        # Plot the signals.
        for i in np.where(df["SIGNAL"])[0]:
            plt.plot(x_values_X[i], self.value_X[i], marker="s", color="r")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_X, self.two_sigma_plus_X, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_X, self.one_sigma_plus_X, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_X, self.cl_Xbar, color="b", label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_X, self.one_sigma_min_X, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_X, self.two_sigma_min_X, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_X, self.lcl_Xbar, color="r", label="LCL")
        plt.title("X bar Chart")

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
        x_values_R = list(range(0, len(self.value_R)))

        # R chart.
        plt.plot(x_values_R, self.value_R, marker="o", color="k", label="R")
        plt.plot(x_values_R, self.ucl_R, color="r", label="UCL")

        # Retrieve the data.
        df = self.data(1)

        # Plot the signals.
        for i in np.where(df["SIGNAL"])[0]:
            plt.plot(x_values_R[i], self.value_R[i], marker="s", color="r")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_R, self.two_sigma_plus_R, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_R, self.one_sigma_plus_R, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_R, self.cl_R, color="b", label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_R, self.one_sigma_min_R, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_R, self.two_sigma_min_R, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_R, self.lcl_R, color="r", label="LCL")
        plt.title("R Chart")

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

        # Initialize the arrays of X bar.
        self.cl_Xbar = np.zeros(((self.number_of_sample), 1))
        self.ucl_Xbar = np.zeros(((self.number_of_sample), 1))
        self.lcl_Xbar = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_X = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_X = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_X = np.zeros(((self.number_of_sample), 1))

        # Initialize the arrays of R.
        self.value_R = np.zeros(((self.number_of_sample), 1))
        self.cl_R = np.zeros(((self.number_of_sample), 1))
        self.ucl_R = np.zeros(((self.number_of_sample), 1))
        self.lcl_R = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_R = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_R = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_R = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_R = np.zeros(((self.number_of_sample), 1))

        # Set the values for X bar and R.
        for i in range(self.number_of_sample):
            self.value_X[i] = self._data[i].mean()
            self.value_R[i] = self._data[i].max() - self._data[i].min()

        # Make the calculations on each split, instead of the full data.
        start_index_X = 0
        start_index_R = 0
        for i in stages:
            # Set the end index.
            end_index_X = i
            end_index_R = i

            # Calculate the UCL, CL, LCL of X.
            self.cl_Xbar[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean()
            self.ucl_Xbar[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() + self._A2 * self.value_R[start_index_R:end_index_R].mean()
            self.lcl_Xbar[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() - self._A2 * self.value_R[start_index_R:end_index_R].mean()

            # Calculate the one and two sigma of X.
            self.two_sigma_plus_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() + self._A2 * self.value_R[start_index_R:end_index_R].mean() * 2/3
            self.one_sigma_plus_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() + self._A2 * self.value_R[start_index_R:end_index_R].mean() * 1/3
            self.one_sigma_min_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() - self._A2 * self.value_R[start_index_R:end_index_R].mean() * 1/3
            self.two_sigma_min_X[start_index_X:end_index_X] = self.value_X[start_index_X:end_index_X].mean() - self._A2 * self.value_R[start_index_R:end_index_R].mean() * 2/3

            # Calculate the  UCL, CL, LCL of R.
            self.cl_R[start_index_R:end_index_R] = self.value_R[start_index_R:end_index_R].mean() 
            self.ucl_R[start_index_R:end_index_R] = self._D4 * self.value_R[start_index_R:end_index_R].mean()
            self.lcl_R[start_index_R:end_index_R] = self._D3 * self.value_R[start_index_R:end_index_R].mean()

            # Calculate the one and two sigma of R.
            self.two_sigma_plus_R[start_index_R:end_index_R] = self.value_R[start_index_R:end_index_R].mean() + (self._D4*self.value_R[start_index_R:end_index_R].mean() - self.value_R[start_index_R:end_index_R].mean()) * 2/3
            self.one_sigma_plus_R[start_index_R:end_index_R] = self.value_R[start_index_R:end_index_R].mean() + (self._D4*self.value_R[start_index_R:end_index_R].mean() - self.value_R[start_index_R:end_index_R].mean()) * 1/3
            self.one_sigma_min_R[start_index_X:end_index_X] = self.value_R[start_index_R:end_index_R].mean() - (self.value_R[start_index_R:end_index_R].mean() - self._D3*self.value_R[start_index_R:end_index_R].mean()) * 1/3
            self.two_sigma_min_R[start_index_X:end_index_X] = self.value_R[start_index_R:end_index_R].mean() - (self.value_R[start_index_R:end_index_R].mean() - self._D3*self.value_R[start_index_R:end_index_R].mean()) * 2/3

            # Set the start index.
            start_index_X = end_index_X
            start_index_R = end_index_R

    def data(self, index:int):
        """ Returns the data.

            :param index: The index for the data (0 = X chart, 1 = mR chart)
        """
        if index == 0: # X chart.
            df = pd.DataFrame(np.column_stack([self.value_X, self.ucl_Xbar, self.two_sigma_plus_X, self.one_sigma_plus_X, self.cl_Xbar, self.one_sigma_min_X, self.two_sigma_min_X, self.lcl_Xbar]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])
            self.execute_rules(df)

            # Check numerical or datetime for the x-axis.
            if (len(super().dates) != 0):
                df['date'] = super().dates
                df=df.set_index('date')

            return df
        if index == 1: # R chart.
            df = pd.DataFrame(np.column_stack([self.value_R, self.ucl_R, self.two_sigma_plus_R, self.one_sigma_plus_R, self.cl_R, self.one_sigma_min_R, self.two_sigma_min_R, self.lcl_R]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])

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
