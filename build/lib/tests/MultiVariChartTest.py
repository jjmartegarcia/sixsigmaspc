"""
The Multi-vari chart.
"""

import numpy as np
from SPC import MultiVariChart

if __name__ == '__main__':
    data = np.array([[23, 25, 24, 26],
                     [22, 26, 24, 25],
                     [28, 28, 22, 23],
                     [25, 25, 26, 36],
                     [22, 22, 25, 26],
                     [26, 24, 23, 22],
                     [29, 24, 24, 24],
                     [26, 25, 25, 22],
                     [22, 25, 24, 24],
                     [25, 22, 26, 24],
                     [24, 24, 24, 23],
                     [24, 25, 26, 23],
                     [22, 28, 22, 26],
                     [23, 24, 25, 26],
                     [24, 25, 29, 24],
                     [24, 22, 28, 26],
                     [24, 25, 25, 25],
                     [22, 24, 25, 26],
                     [26, 25, 22, 24],
                     [26, 22, 24, 25]])

    # The Multi-vari chart.
    chart = MultiVariChart(data=data)
    chart.plot()
