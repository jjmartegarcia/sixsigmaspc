"""
An Individual moving range (I-MR) chart is used when data is continuous and not collected in subgroups.
An I-MR chart provides process variation over time in graphical method.
I-MR chart is basically two separate charts – Individuals (I) chart and Moving Range (MR) chart, the combination of two charts provides the complete picture of process behavior.

I-Chart: Individual chart displays the individual data points and monitors mean and shifts in
the process when the data points collected at regular intervals of time. This chart will help to
identify the common and assignable causes in the process, if any.

MR Chart: While Individual chart monitors the process mean, the Moving Range chart monitors the
process variation when the data points collected at regular intervals of time. In other words the
moving range chart tracks the absolute difference of each measurement to its previous measurement.

https://sixsigmastudyguide.com/i-mr-chart/
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime
from SPC import ControlChart

class ImRControlChart(ControlChart):
    _E2 : float # The Control Chart E2 constant.
    _d2 : float # The Control Chart d2 constant.
    _D3 : float # The Control Chart D3 constant.
    _D4 : float # The Control Chart D4 constant.

    def __init__(self, data:list, xlabel:str="", ylabel_top:str="", ylabel_bottom:str=""):
        """ Initialization.

            :param data: values.
            :param xlabel: x-as label.
            :param ylabel_top: top y-as label.
            :param ylabel_bottom: bottom y-as label.
        """
        # Initialization of the base class.
        super().__init__(2) # X chart and mR chart.

        # Remember the parameters.
        self._data = data
        self._xlabel = xlabel
        self._ylabel_top = ylabel_top
        self._ylabel_bottom = ylabel_bottom

        # Remember the Control chart constants size=2 (comparing the current state with previous state).
        self._E2 = 2.66
        self._d2 = 1.128
        self._D3 = 0
        self._D4 = 3.267

        # The number of samples.
        self.number_of_sample = len(data)

        # Set the values array.
        self.value_I = data

        # Initialize the arrays of I.
        self.cl_I = np.zeros(((self.number_of_sample), 1))
        self.ucl_I = np.zeros(((self.number_of_sample), 1))
        self.lcl_I = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_I = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_I = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_I = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_I = np.zeros(((self.number_of_sample), 1))

        # Initialize the arrays of mR.
        self.value_mR = np.zeros(((self.number_of_sample - 1), 1))
        self.cl_mR = np.zeros(((self.number_of_sample - 1), 1))
        self.ucl_mR = np.zeros(((self.number_of_sample - 1), 1))
        self.lcl_mR = np.zeros(((self.number_of_sample - 1), 1))
        self.two_sigma_plus_mR = np.zeros(((self.number_of_sample - 1), 1))
        self.one_sigma_plus_mR = np.zeros(((self.number_of_sample - 1), 1))
        self.two_sigma_min_mR = np.zeros(((self.number_of_sample - 1), 1))
        self.one_sigma_min_mR = np.zeros(((self.number_of_sample - 1), 1))

        # Calculate the difference between the samples.
        for i in range(self.number_of_sample - 1):
            self.value_mR[i]=abs(self.value_I[i+1] - self.value_I[i])

        # Calculate the UCL, CL, LCL of I.
        self.cl_I[:] = self.value_I.mean() 
        self.ucl_I[:] = self.value_I.mean() + self._E2 * self.value_mR.mean()
        self.lcl_I[:] = self.value_I.mean() - self._E2 * self.value_mR.mean()

        # Calculate the one and two sigma of I.
        self.two_sigma_plus_I[:] = self.value_I.mean() + self._E2 * self.value_mR.mean() * 2/3
        self.one_sigma_plus_I[:] = self.value_I.mean() + self._E2 * self.value_mR.mean() * 1/3
        self.one_sigma_min_I[:] = self.value_I.mean() - self._E2 * self.value_mR.mean() * 1/3
        self.two_sigma_min_I[:] = self.value_I.mean() - self._E2 * self.value_mR.mean() * 2/3

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
            x_values_I = list(range(0, len(self.value_I)))
        else:
            format=super().dateformat
            x_values_I = [datetime.strptime(d, format).date() for d in super().dates]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(super().dateformat))

        # I chart.
        plt.plot(x_values_I, self.value_I, marker="o", color="k", label="I")
        plt.plot(x_values_I, self.ucl_I, color="r", label="UCL")

        # Retrieve the data.
        df = self.data(0)

        # Plot the signals.
        for i in np.where(df["SIGNAL"])[0]:
            plt.plot(x_values_I[i], self.value_I[i], marker="s", color="r")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_I, self.two_sigma_plus_I, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_I, self.one_sigma_plus_I, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_I, self.cl_I, color="b", label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_I, self.one_sigma_min_I, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_I, self.two_sigma_min_I, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_I, self.lcl_I, color="r", label="LCL")
        plt.title("I Chart")

        # Add a legend.
        plt.legend(loc='upper right')

        # Set the y-label.
        plt.ylabel( self._ylabel_top)

        # The 2nd vertical plot.
        plt.subplot(2,1,2)

        # The x-axis can be numeric or datetime.
        if (len(super().dates) == 0):
            x_values_mR = list(range(1, len(self.value_I)))
        else:
            format=super().dateformat
            x_values_mR = [datetime.strptime(d, format).date() for d in super().dates][1:]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(super().dateformat))

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

        # Add a legend.
        plt.legend(loc='upper right')

        # Set the y-label.
        plt.ylabel(self._ylabel_bottom)

        # Set the x-label.
        plt.xlabel( self._xlabel)

        # Show the plot.
        plt.show()

    def split(self, stages:list):
        """ Split the chart.

            :param stages: The stages.
        """
        # Include the last index.
        if not self.number_of_sample in stages:
            stages.append(self.number_of_sample)

        # Initialize the arrays of I.
        self.cl_I = np.zeros(((self.number_of_sample), 1))
        self.ucl_I = np.zeros(((self.number_of_sample), 1))
        self.lcl_I = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_plus_I = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_plus_I = np.zeros(((self.number_of_sample), 1))
        self.two_sigma_min_I = np.zeros(((self.number_of_sample), 1))
        self.one_sigma_min_I = np.zeros(((self.number_of_sample), 1))

        # Initialize the arrays of mR.
        self.value_mR = np.zeros(((self.number_of_sample-1), 1))
        self.cl_mR = np.zeros(((self.number_of_sample-1), 1))
        self.ucl_mR = np.zeros(((self.number_of_sample-1), 1))
        self.lcl_mR = np.zeros(((self.number_of_sample-1), 1))

        # Calculate the difference between the samples.
        for i in range(self.number_of_sample-1):
            self.value_mR[i]=abs(self.value_I[i+1] - self.value_I[i])

        # Make the calculations on each split, instead of the full data.
        start_index_I = 0
        start_index_mR = 0
        for i in stages:
            # Set the end index.
            end_index_I = i
            end_index_mR = i-1

            # Calculate the UCL, CL, LCL of I.
            self.cl_I[start_index_I:end_index_I] = self.value_I[start_index_I:end_index_I].mean() 
            self.ucl_I[start_index_I:end_index_I] = self.value_I[start_index_I:end_index_I].mean() + self._E2 * self.value_mR[start_index_mR:end_index_mR].mean()
            self.lcl_I[start_index_I:end_index_I] = self.value_I[start_index_I:end_index_I].mean() - self._E2 * self.value_mR[start_index_mR:end_index_mR].mean()

            # Calculate the one and two sigma of I.
            self.two_sigma_plus_I[start_index_I:end_index_I] = self.value_I[start_index_I:end_index_I].mean() + self._E2 * self.value_mR[start_index_mR:end_index_mR].mean() * 2/3
            self.one_sigma_plus_I[start_index_I:end_index_I] = self.value_I[start_index_I:end_index_I].mean() + self._E2 * self.value_mR[start_index_mR:end_index_mR].mean() * 1/3
            self.one_sigma_min_I[start_index_I:end_index_I] = self.value_I[start_index_I:end_index_I].mean() - self._E2 * self.value_mR[start_index_mR:end_index_mR].mean() * 1/3
            self.two_sigma_min_I[start_index_I:end_index_I] = self.value_I[start_index_I:end_index_I].mean() - self._E2 * self.value_mR[start_index_mR:end_index_mR].mean() * 2/3

            # Calculate the  UCL, CL, LCL of mR.
            self.cl_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() 
            self.ucl_mR[start_index_mR:end_index_mR] = self._D4*self.value_mR[start_index_mR:end_index_mR].mean()
            self.lcl_mR[start_index_mR:end_index_mR] = self._D3*self.value_mR[start_index_mR:end_index_mR].mean()

            # Calculate the one and two sigma of mR.
            self.two_sigma_plus_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() + (self._D4 * self.value_mR[start_index_mR:end_index_mR].mean() - self.value_mR[start_index_mR:end_index_mR].mean()) * 2/3
            self.one_sigma_plus_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() + (self._D4 * self.value_mR[start_index_mR:end_index_mR].mean() - self.value_mR[start_index_mR:end_index_mR].mean()) * 1/3
            self.one_sigma_min_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() - (self.value_mR[start_index_mR:end_index_mR].mean() - self._D3 * self.value_mR[start_index_mR:end_index_mR].mean()) * 1/3
            self.two_sigma_min_mR[start_index_mR:end_index_mR] = self.value_mR[start_index_mR:end_index_mR].mean() - (self.value_mR[start_index_mR:end_index_mR].mean() - self._D3 * self.value_mR[start_index_mR:end_index_mR].mean()) * 2/3

            # Set the start index.
            start_index_I = end_index_I
            start_index_mR = end_index_mR

    def data(self, index:int):
        """ Returns the data.

            :param index: The index for the data (0 = X chart, 1 = mR chart)
        """
        if index == 0: # X chart.
            df = pd.DataFrame(np.column_stack([self.value_I, self.ucl_I, self.two_sigma_plus_I, self.one_sigma_plus_I, self.cl_I, self.one_sigma_min_I, self.two_sigma_min_I, self.lcl_I]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])
            self.execute_rules(df)

            # Check numerical or datetime for the x-axis.
            if (len(super().dates) != 0):
                df['date'] = super().dates
                df=df.set_index('date')

            return df
        if index == 1: # R chart.
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
