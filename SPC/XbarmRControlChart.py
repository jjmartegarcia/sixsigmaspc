"""

"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from SPC import ControlChart
from SPC import XbarRControlChartConstants

class XbarmRControlChart(ControlChart):
    _A2 : float # The Control Chart A2 constant.
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
        super().__init__(2) # X bar chart and mR chart.

        # Remember the parameters.
        self._data = data
        self._xlabel = xlabel
        self._ylabel_top = ylabel_top
        self._ylabel_bottom = ylabel_bottom

        # Determine the subgroup size.
        n = len(data[0])

        # Set the values array.
        self.value_X = data

        # The number of samples.
        self.number_of_sample = len(data)

        # Initialize the sample averages.
        self._sample_average = np.zeros(((self.number_of_sample), 1))

        # Calculate the sample averages.
        for i in range(self.number_of_sample):
            self._sample_average[i]=np.average(data[i])

        # Initialize the moving range average.
        self._value_mR_average = np.zeros(((self.number_of_sample -1), 1))

        # Calculate the moving range average.
        for i in range(self.number_of_sample -1):
            self._value_mR_average[i]=abs(self._sample_average[i+1] - self._sample_average[i])

        # Initialize the range.
        self._range = np.zeros(((self.number_of_sample), 1))

        # Calculate the range.
        for i in range(self.number_of_sample):
            self._range[i]=np.max(data[i]) - np.min(data[i])

        # Initialize the moving range.
        self._value_mR = np.zeros(((self.number_of_sample -1), 1))

        # Calculate the moving range average.
        for i in range(self.number_of_sample -1):
            self._value_mR[i]=abs(self._range[i+1] - self._range[i])

        # Initialize the arrays of X bar (MR method).
        self.cl_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.ucl_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.lcl_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_plus_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_plus_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_min_Xmr = np.zeros(((self.number_of_sample) -1, 1))
        self.one_sigma_min_Xmr = np.zeros(((self.number_of_sample -1), 1))

        # Initialize the arrays of R (MR method).
        self.cl_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.ucl_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.lcl_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_plus_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_plus_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_min_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_min_Rmr = np.zeros(((self.number_of_sample -1), 1))

        # Calculate the UCL, CL, LCL of X bar (MR method).
        self.cl_Xmr[:] = self._sample_average.mean()
        self.ucl_Xmr[:] = self._sample_average.mean() + 2.66 * self._value_mR_average.mean()
        self.lcl_Xmr[:] = max(0, self._sample_average.mean() - 2.66 * self._value_mR_average.mean())

        # Calculate the one and two sigma of X bar (MR method).
        self.two_sigma_plus_Xmr[:] = self._sample_average.mean() + 2.66 * self._value_mR_average.mean() * 2/3
        self.one_sigma_plus_Xmr[:] = self._sample_average.mean() + 2.66 * self._value_mR_average.mean() * 1/3
        self.one_sigma_min_Xmr[:] = max(0, self._sample_average.mean() - 2.66 * self._value_mR_average.mean() * 1/3)
        self.two_sigma_min_Xmr[:] = max(0, self._sample_average.mean() - 2.66 * self._value_mR_average.mean() * 2/3)

        # Calculate the UCL, CL, LCL of R (MR method).
        self.cl_Rmr[:] = self._range.mean() 
        self.ucl_Rmr[:] = self._range.mean() + 2.66 * self._value_mR.mean()
        self.lcl_Rmr[:] = max(0, self._range.mean() - 2.66 * self._value_mR.mean())

        # Calculate the one and two sigma of R (MR method).
        self.two_sigma_plus_Rmr[:] = self._range.mean() + 2.66 * self._value_mR.mean() * 2/3
        self.one_sigma_plus_Rmr[:] = self._range.mean() + 2.66 * self._value_mR.mean() * 1/3
        self.one_sigma_min_Rmr[:] = max(0, self._range.mean() - 2.66 * self._value_mR.mean() * 1/3)
        self.two_sigma_min_Rmr[:] = max(0, self._range.mean() - 2.66 * self._value_mR.mean() * 2/3)

    def plot(self):
        """ Create the plot.
        """
        plt.figure(figsize=(15,10))

        # The 1st vertical plot.
        plt.subplot(2,1,1)

        # The x-axis can be numeric or datetime.
        if (len(super().dates) == 0):
            x_values_X = list(range(0, len(self._value_mR_average)))
        else:
            format=super().dateformat
            x_values_X = [datetime.strptime(d, format).date() for d in super().dates][1:]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(super().dateformat))

        # X chart.
        plt.plot(x_values_X, self._value_mR_average, marker="o", color="k", label="X")
        plt.plot(x_values_X, self.ucl_Xmr, color="r", label="UCL")

        # Retrieve the data.
        df = self.data(0)

        # Plot the signals.
        for i in np.where(df["SIGNAL"])[0]:
            plt.plot(x_values_X[i], self._value_mR_average[i], marker="s", color="r")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_X, self.two_sigma_plus_Xmr, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_X, self.one_sigma_plus_Xmr, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_X, self.cl_Xmr, color="b", label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_X, self.one_sigma_min_Xmr, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_X, self.two_sigma_min_Xmr, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_X, self.lcl_Xmr, color="r", label="LCL")
        plt.title("X (MR) Chart")

        # Set the lower and upper limits for the x-axis.
        plt.xlim(min(x_values_X), max(x_values_X))

        # Add a legend.
        plt.legend(loc='upper right')

        # Set the y-label.
        plt.ylabel( self._ylabel_top)

        # The 2nd vertical plot.
        plt.subplot(2,1,2)

        # The x-axis can be numeric or datetime.
        if (len(super().dates) == 0):
            x_values_mR = list(range(0, len(self._value_mR)))
        else:
            format=super().dateformat
            x_values_mR = [datetime.strptime(d, format).date() for d in super().dates][1:]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(super().dateformat))

        # R (MR method) chart.
        plt.plot(x_values_mR, self._value_mR, marker="o", color="k", label="R")
        plt.plot(x_values_mR, self.ucl_Rmr, color="r", label="UCL")

        # Retrieve the data.
        df = self.data(1)

        # Plot the signals.
        for i in np.where(df["SIGNAL"])[0]:
            plt.plot(x_values_mR[i], self._value_mR[i], marker="s", color="r")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_mR, self.two_sigma_plus_Rmr, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_mR, self.one_sigma_plus_Rmr, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_mR, self.cl_Rmr, color="b", label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_mR, self.one_sigma_min_Rmr, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_mR, self.two_sigma_min_Rmr, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_mR, self.lcl_Rmr, color="r", label="LCL")
        plt.title("R (MR) Chart")

        # Set the lower and upper limits for the x-axis.
        plt.xlim(min(x_values_X), max(x_values_X))

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

        # Initialize the arrays of X bar (MR method).
        self.cl_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.ucl_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.lcl_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_plus_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_plus_Xmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_min_Xmr = np.zeros(((self.number_of_sample) -1, 1))
        self.one_sigma_min_Xmr = np.zeros(((self.number_of_sample -1), 1))

        # Initialize the arrays of R (MR method).
        self.cl_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.ucl_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.lcl_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_plus_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_plus_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.two_sigma_min_Rmr = np.zeros(((self.number_of_sample -1), 1))
        self.one_sigma_min_Rmr = np.zeros(((self.number_of_sample -1), 1))

        # Initialize the sample averages.
        self._sample_average = np.zeros(((self.number_of_sample), 1))

        # Calculate the sample averages.
        for i in range(self.number_of_sample):
            self._sample_average[i]=np.average(self.value_X[i])

        # Initialize the moving range average.
        self._value_mR_average = np.zeros(((self.number_of_sample -1), 1))

        # Calculate the moving range average.
        for i in range(self.number_of_sample -1):
            self._value_mR_average[i]=abs(self._sample_average[i+1] - self._sample_average[i])

        # Initialize the range.
        self._range = np.zeros(((self.number_of_sample), 1))

        # Calculate the range.
        for i in range(self.number_of_sample):
            self._range[i]=np.max(self.value_X[i]) - np.min(self.value_X[i])

        # Initialize the moving range.
        self._value_mR = np.zeros(((self.number_of_sample -1), 1))

        # Calculate the moving range average.
        for i in range(self.number_of_sample -1):
            self._value_mR[i]=abs(self._range[i+1] - self._range[i])

        # Make the calculations on each split, instead of the full data.
        start_index_mR = 0
        start_index_Rmr = 0
        for i in stages:
            # Set the end index.
            end_index_mR = i
            end_index_Rmr = i

            print(f'start_index_mR={start_index_mR}, end_index_mR={end_index_mR}')
            print(f'start_index_Rmr={start_index_Rmr}, end_index_Rmr={end_index_Rmr}')

            # Calculate the UCL, CL, LCL of X bar (MR method).
            self.cl_Xmr[start_index_mR:end_index_mR] = self._sample_average[start_index_mR:end_index_mR].mean()
            self.ucl_Xmr[start_index_mR:end_index_mR] = self._sample_average[start_index_mR:end_index_mR].mean() + 2.66 * self._value_mR_average[start_index_mR:end_index_mR].mean()
            self.lcl_Xmr[start_index_mR:end_index_mR] = max(0, self._sample_average[start_index_mR:end_index_mR].mean() - 2.66 * self._value_mR_average[start_index_mR:end_index_mR].mean())

            # Calculate the one and two sigma of X bar (MR method).
            self.two_sigma_plus_Xmr[start_index_mR:end_index_mR] = self._sample_average[start_index_mR:end_index_mR].mean() + 2.66 * self._value_mR_average[start_index_mR:end_index_mR].mean() * 2/3
            self.one_sigma_plus_Xmr[start_index_mR:end_index_mR] = self._sample_average[start_index_mR:end_index_mR].mean() + 2.66 * self._value_mR_average[start_index_mR:end_index_mR].mean() * 1/3
            self.one_sigma_min_Xmr[start_index_mR:end_index_mR] = max(0, self._sample_average[start_index_mR:end_index_mR].mean() - 2.66 * self._value_mR_average[start_index_mR:end_index_mR].mean() * 1/3)
            self.two_sigma_min_Xmr[start_index_mR:end_index_mR] = max(0, self._sample_average[start_index_mR:end_index_mR].mean() - 2.66 * self._value_mR_average[start_index_mR:end_index_mR].mean() * 2/3)

            # Calculate the UCL, CL, LCL of R (MR method).
            self.cl_Rmr[start_index_Rmr:end_index_Rmr] = self._range[start_index_Rmr:end_index_Rmr].mean() 
            self.ucl_Rmr[start_index_Rmr:end_index_Rmr] = self._range[start_index_Rmr:end_index_Rmr].mean() + 2.66 * self._value_mR[start_index_Rmr:end_index_Rmr].mean()
            self.lcl_Rmr[start_index_Rmr:end_index_Rmr] = max(0, self._range[start_index_Rmr:end_index_Rmr].mean() - 2.66 * self._value_mR[start_index_Rmr:end_index_Rmr].mean())

            # Calculate the one and two sigma of R (MR method).
            self.two_sigma_plus_Rmr[start_index_Rmr:end_index_Rmr] = self._range[start_index_Rmr:end_index_Rmr].mean() + 2.66 * self._value_mR[start_index_Rmr:end_index_Rmr].mean() * 2/3
            self.one_sigma_plus_Rmr[start_index_Rmr:end_index_Rmr] = self._range[start_index_Rmr:end_index_Rmr].mean() + 2.66 * self._value_mR[start_index_Rmr:end_index_Rmr].mean() * 1/3
            self.one_sigma_min_Rmr[start_index_Rmr:end_index_Rmr] = max(0, self._range[start_index_Rmr:end_index_Rmr].mean() - 2.66 * self._value_mR[start_index_Rmr:end_index_Rmr].mean() * 1/3)
            self.two_sigma_min_Rmr[start_index_Rmr:end_index_Rmr] = max(0, self._range[start_index_Rmr:end_index_Rmr].mean() - 2.66 * self._value_mR[start_index_Rmr:end_index_Rmr].mean() * 2/3)

            # Set the start index.
            start_index_mR = end_index_mR
            start_index_Rmr = end_index_Rmr

    def data(self, index:int):
        """ Returns the data.

            :param index: The index for the data (0 = X chart, 1 = mR chart)
        """
        if index == 0: # X chart.
            df = pd.DataFrame(np.column_stack([self._value_mR_average, self.ucl_Xmr, self.two_sigma_plus_Xmr, self.one_sigma_plus_Xmr, self.cl_Xmr, self.one_sigma_min_Xmr, self.two_sigma_min_Xmr, self.lcl_Xmr]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])
            self.execute_rules(df)

            # Check numerical or datetime for the x-axis.
            if (len(super().dates) != 0):
                df['date'] = super().dates[1:]
                df=df.set_index('date')

            return df
        if index == 1: # mR chart.
            df = pd.DataFrame(np.column_stack([self._value_mR, self.ucl_Rmr, self.two_sigma_plus_Rmr, self.one_sigma_plus_Rmr, self.cl_Rmr, self.one_sigma_min_Rmr, self.two_sigma_min_Rmr, self.lcl_Rmr]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])
            self.execute_rules(df)

            # Check numerical or datetime for the x-axis.
            if (len(super().dates) != 0):
                df['date'] = super().dates[1:]
                df=df.set_index('date')

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

    def normally_distributed(self, significance_level:float):
        """ Check if the data follows normal distribution.
            Returns true when the data did not show evidence of non-normality.
            Returns false when the data is not normally distributed.

            :param significance_level: significance level.
        """
        return self._normally_distributed(self._sample_average, significance_level)

    def auto_correlated(self, delay:int, threshold:float):
        """ Check if the data has a correlation with itself for a specific delay.
            Returns true when the data is correlated with itself.
            Returns false when the data is not correlated with itself.

            :param delay: delay.
            :param threshold: correlation threshold.
        """
        return self._auto_correlated(self._sample_average, delay, threshold)
