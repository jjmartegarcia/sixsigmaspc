"""
The Multi-vari chart.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

class MultiVariChart():
    _dateformat = "%Y-%m-%d" # The date format.
    _dates = [] # The dates.

    def __init__(self, data:list, xlabel:str="", ylabel:str=""):
        """ Initialization.

            :param data: The data.
            :param xlabel: x-as label.
            :param ylabel: y-as label.
        """
        # Remember the parameters.
        self._data=data
        self._xlabel = xlabel
        self._ylabel = ylabel

        # The number of samples.
        self.number_of_sample = len(data)

        # Initialize the arrays of X bar.
        self.value_X = np.zeros(((self.number_of_sample), 1))

        # Set the values.
        for i in range(self.number_of_sample):
            self.value_X[i] = data[i].mean()

    def plot(self):
        """ Create the plot.
        """
        plt.figure(figsize=(15,10))

        # The x-axis can be numeric or datetime.
        if (len(self._dates) == 0):
            x_values_X = list(range(0, len(self.value_X)))
        else:
            format=self._dateformat
            x_values_X = [datetime.strptime(d, format).date() for d in self._dates]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(self._dateformat))

        # Plot the vertical lines with min/max.
        for i in range(self.number_of_sample):
            plt.vlines(x_values_X[i], self._data[i].min(), self._data[i].max(), color='lightgrey', linewidth=4)

        plt.plot(x_values_X, self.value_X, marker="o", color="blue", label="")
        plt.title("Multi-Vari Chart")

        # Set the x-label.
        plt.xlabel( self._xlabel)

        # Set the y-label.
        plt.ylabel( self._ylabel)

        plt.show()

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
