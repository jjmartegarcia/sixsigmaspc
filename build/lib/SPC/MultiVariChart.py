"""
The Multi-vari chart.
"""

import numpy as np
import matplotlib.pyplot as plt

class MultiVariChart():
    def __init__(self, data:list):
        """ Initialization.

            :param data: The data.
        """
        # Remember the parameters.
        self._data=data

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
        x_values_X = list(range(0, len(self.value_X)))

        # Plot the vertical lines with min/max.
        for i in range(self.number_of_sample):
            plt.vlines(x_values_X[i], self._data[i].min(), self._data[i].max(), color='lightgrey', linewidth=4)

        plt.plot(x_values_X, self.value_X, marker="o", color="blue", label="")
        plt.xticks(np.arange(len(self.value_X)))
        plt.title("Multi-Vari Chart")
        plt.show()
