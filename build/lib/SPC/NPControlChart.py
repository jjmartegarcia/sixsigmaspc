"""
Attribute chart: np chart is also known as the control chart for defectives (d-chart).

https://sixsigmastudyguide.com/attribute-chart-np-chart/
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime
from SPC import ControlChart

class NPControlChart(ControlChart):
    def __init__(self, c:list, n:list):
        """ Initialization.

            :param c: number of defects in the samples.
            :param n: sample sizes.
        """
        # Initialization of the base class.
        super().__init__(1) # NP chart.

        # The number of defects.
        self.number_of_defects = len(c)

        # Remember the number of defective in the sample.
        self.c = c

        # Remember the sample sizes.
        self.n = n

        # Initialize the arrays.
        self.value_p = np.zeros(((self.number_of_defects), 1))
        self.cl_p = np.zeros(((self.number_of_defects), 1))
        self.ucl_p = np.zeros(((self.number_of_defects), 1))
        self.lcl_p = np.zeros(((self.number_of_defects), 1))
        self.two_sigma_plus = np.zeros(((self.number_of_defects), 1))
        self.one_sigma_plus = np.zeros(((self.number_of_defects), 1))
        self.two_sigma_min = np.zeros(((self.number_of_defects), 1))
        self.one_sigma_min = np.zeros(((self.number_of_defects), 1))

        # Set the values.
        for i in range(self.number_of_defects):
            self.value_p[i] = c[i]

        # Calculate the UCL, CL, LCL.
        self.cl_p[:] = self.value_p.mean()
        self.ucl_p[:] = self.value_p.mean() + 3 * np.sqrt(self.value_p.mean() * (1 - self.c.sum() / self.n.sum()))
        self.lcl_p[:] = max(self.value_p.mean() - 3 * np.sqrt(self.value_p.mean() * (1 - self.c.sum() / self.n.sum())), 0.0)

        # Calculate the one and two sigma.
        self.two_sigma_plus[:] = self.value_p.mean() + 3 * np.sqrt(self.value_p.mean() * (1 - self.c.sum() / self.n.sum())) * 2/3
        self.one_sigma_plus[:] = self.value_p.mean() + 3 * np.sqrt(self.value_p.mean() * (1 - self.c.sum() / self.n.sum())) * 1/3
        self.one_sigma_min[:] = max(self.value_p.mean() - 3 * np.sqrt(self.value_p.mean() * (1 - self.c.sum() / self.n.sum())) * 1/3, 0.0)
        self.two_sigma_min[:] = max(self.value_p.mean() - 3 * np.sqrt(self.value_p.mean() * (1 - self.c.sum() / self.n.sum())) * 2/3, 0.0)

    def plot(self):
        """ Create the P chart.
        """
        # The x-axis can be numeric or datetime.
        if (len(super().dates) == 0):
            x_values_p = list(range(0, self.number_of_defects))
        else:
            format=super().dateformat
            x_values_p = [datetime.strptime(d, format).date() for d in super().dates]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(super().dateformat))

        # NP chart.
        plt.figure(figsize=(15,5))
        plt.plot(x_values_p, self.value_p, marker="o",color="k",label="p")
        plt.plot(x_values_p, self.ucl_p,color="r",label="UCL")

        # The limits indicator for +2s, +1s.
        if super().limits:
            plt.plot(x_values_p, self.two_sigma_plus, color="r", linestyle='dashed', label="+2s")
            plt.plot(x_values_p, self.one_sigma_plus, color="r", linestyle='dashed', label="+1s")

        plt.plot(x_values_p, self.cl_p,color="b",label="CL")

        # The limits indicator for -1s, -2s.
        if super().limits:
            plt.plot(x_values_p, self.one_sigma_min, color="r", linestyle='dashed', label="-1s")
            plt.plot(x_values_p, self.two_sigma_min, color="r", linestyle='dashed', label="-2s")

        plt.plot(x_values_p, self.lcl_p,color="r",label="LCL")
        plt.title("P Control Chart")

        # Check numerical or datetime for the x-axis.
        if (len(super().dates) == 0):
            plt.xticks(np.arange(self.number_of_defects))
        else:
            plt.xticks(rotation=45, ha='right')
        
        # Add a legend.
        plt.legend(loc='upper right')

        plt.show()

    def split(self, stages:list):
        """ Split the chart.

            :param stages: The stages.
        """
        # Include the last index.
        if not self.number_of_defects in stages:
            stages.append(self.number_of_defects)

        # Initialize the arrays.
        self.cl_p = np.zeros(((self.number_of_defects), 1))
        self.ucl_p = np.zeros(((self.number_of_defects), 1))
        self.lcl_p = np.zeros(((self.number_of_defects), 1))
        self.two_sigma_plus = np.zeros(((self.number_of_defects), 1))
        self.one_sigma_plus = np.zeros(((self.number_of_defects), 1))
        self.two_sigma_min = np.zeros(((self.number_of_defects), 1))
        self.one_sigma_min = np.zeros(((self.number_of_defects), 1))

        # Make the calculations on each split, instead of the full data.
        start_index = 0
        for i in stages:
            # Set the end index.
            end_index = i

            # Calculate the UCL, CL, LCL.
            self.cl_p[start_index:end_index] = self.value_p[start_index:end_index].mean()
            self.ucl_p[start_index:end_index] = self.value_p[start_index:end_index].mean() + 3 * np.sqrt(self.value_p[start_index:end_index].mean() * (1 - self.c[start_index:end_index].sum() / self.n[start_index:end_index].sum()))
            self.lcl_p[start_index:end_index] = self.value_p[start_index:end_index].mean() - 3 * np.sqrt(self.value_p[start_index:end_index].mean() * (1 - self.c[start_index:end_index].sum() / self.n[start_index:end_index].sum()))

            # Calculate the one and two sigma.
            self.two_sigma_plus[start_index:end_index] = self.value_p[start_index:end_index].mean() + 3 * np.sqrt(self.value_p[start_index:end_index].mean() * (1 - self.c[start_index:end_index].sum() / self.n[start_index:end_index].sum())) * 2/3
            self.one_sigma_plus[start_index:end_index] = self.value_p[start_index:end_index].mean() + 3 * np.sqrt(self.value_p[start_index:end_index].mean() * (1 - self.c[start_index:end_index].sum() / self.n[start_index:end_index].sum())) * 1/3
            self.one_sigma_min[start_index:end_index] = max(self.value_p[start_index:end_index].mean() - 3 * np.sqrt(self.value_p[start_index:end_index].mean() * (1 - self.c[start_index:end_index].sum() / self.n[start_index:end_index].sum())) * 1/3, 0.0)
            self.two_sigma_min[start_index:end_index] = max(self.value_p[start_index:end_index].mean() - 3 * np.sqrt(self.value_p[start_index:end_index].mean() * (1 - self.c[start_index:end_index].sum() / self.n[start_index:end_index].sum())) * 2/3, 0.0)

            # Set the start index.
            start_index = end_index

    def data(self, index:int):
        """ Returns the data.

            :param index: The index for the data (0 = NP chart)
        """
        if index == 0: # NP chart.
            df = pd.DataFrame(np.column_stack([self.value_p, self.ucl_p, self.two_sigma_plus, self.one_sigma_plus, self.cl_p, self.one_sigma_min, self.two_sigma_min, self.lcl_p]), columns=['value', 'UCL', '+2s', '+1s', 'CL', '-1s', '-2s', 'LCL'])
            self.execute_rules(df)

            # Check numerical or datetime for the x-axis.
            if (len(super().dates) != 0):
                df['date'] = super().dates
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

        return True
