"""
The Process Capability chart.
"""

import numpy as np
import matplotlib.pyplot as plt
import statistics

class ProcessCapabilityChart():
    def __init__(self, data:list, target:int, LSL:int, USL:int):
        """ Initialization.

            :param data: The data.
            :param target: The target.
            :param LSL: The lower specification limit.
            :param USL: The upper specification limit.
        """
        # Remember the parameters.
        self._data=data
        self._target = target
        self._LSL = LSL
        self._USL = USL

        # Calculate Cp.
        self.Cp = (USL-LSL)/(6*np.std(data))

        # Calculate Cpk.
        self.Cpk = min((USL-statistics.mean(data))/(3*statistics.stdev(data)), (statistics.mean(data)-LSL)/(3*statistics.stdev(data)))

        # Get data summary statistics.
        self.num_samples = len(data)
        self.sample_mean = statistics.mean(data)
        self.sample_std = statistics.stdev(data)
        self.sample_max = max(data)
        self.sample_min = min(data)
        self.sample_median = statistics.median(data)

        # Get percentages outside the specification limits.
        self.pct_below_LSL = len([item for item in data if item < LSL])/self.num_samples*100
        self.pct_above_USL = len([item for item in data if item > USL])/self.num_samples*100
        self.reject_rate = self.pct_below_LSL + self.pct_above_USL

    def plot(self, bins:int):
        """ Create the plot.

            :param bins: The number of bins.
        """
        plt.figure(figsize=(15,10))
        plt.hist(self._data, bins=bins, color="lightgrey", edgecolor="black", density=False)
        plt.axvline(self._LSL, linestyle="dashed", color="red", label="LSL")
        plt.axvline(self._target, linestyle="dashed", color="grey", label="Target")
        plt.axvline(self._USL, linestyle="dashed", color="red", label="USL")
        plt.title("Histogram")
        plt.legend()
        plt.show()

    def capable(self, target_cpk:float):
        """ Returns the capable indicator.

            :param target_cpk: The target Cpk value.
        """
        return self.Cpk > target_cpk
