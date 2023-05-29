"""
The Process Capability chart.
"""

import numpy as np
from SPC import ProcessCapabilityChart

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

    # Flatten the data.
    data_flat = np.concatenate(data).ravel().tolist()

    # The Process Capability chart.
    capability = ProcessCapabilityChart(data=data_flat, target=23, LSL=21, USL=28)
    capability.plot(bins=8)
    print("Cp={0}".format(capability.Cp))
    print("Cpk={0}".format(capability.Cpk))
    print("samples={0}".format(capability.num_samples))
    print("mean={0}".format(capability.sample_mean))
    print("stdev={0}".format(capability.sample_std))
    print("max={0}".format(capability.sample_max))
    print("min={0}".format(capability.sample_min))
    print("mean={0}".format(capability.sample_median))
    print("pct_below_LSL={0}".format(capability.pct_below_LSL))
    print("pct_above_USL={0}".format(capability.pct_above_USL))
    print("reject_rate={0}".format(capability.reject_rate))
    print("capable={0}".format(capability.capable(target_cpk=1.33)))
