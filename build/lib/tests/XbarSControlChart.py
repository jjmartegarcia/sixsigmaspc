"""
X Bar S charts are control charts to examine the process mean and standard deviation over the time.

X-bar chart: The mean or average change in process over time from subgroup values.
The control limits on the X-Bar brings the sample’s mean and center into consideration.

S-chart: The standard deviation of the process over the time from subgroups values.
This monitors the process standard deviation (as approximated by the sample moving range).

https://sixsigmastudyguide.com/x-bar-s-chart/
"""

import numpy as np
from SPC import Rule01
from SPC import Rule02
from SPC import Rule03
from SPC import Rule04
from SPC import Rule05
from SPC import Rule06
from SPC import Rule07
from SPC import Rule08
from SPC import XbarSControlChart

if __name__ == '__main__':
    data = np.array([[34,35,35,34],
                    [37,35,25,32],
                    [36,35,35,34],
                    [33,36,35,35],
                    [36,33,34,35],
                    [33,36,35,35],
                    [36,36,35,33],
                    [33,35,35,34],
                    [36,36,35,33],
                    [34,36,36,34],
                    [36,35,33,35],
                    [35,35,35,36]])
    dates = ['21-12-21', '22-12-21', '23-12-21', '24-12-21', '25-12-21', '26-12-21', '27-12-21', '28-12-21', '29-12-21','30-12-21', '31-12-21', '01-01-22']
    chart = XbarSControlChart(data=data, xlabel="x-label", ylabel_top="y-label-top", ylabel_bottom="y-label-bottom")
    normally_distributed=chart.normally_distributed(data=chart.value_X, significance_level=0.05)
    print("normally_distributed={0}".format(normally_distributed))
    chart.dates = dates
    chart.dateformat = "%d-%m-%y"
    #stages=chart.stages(data=chart.value_X, max_stages=4)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([2, 12])
    #chart.limits=True
    chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])
    chart.plot()

    df1 = chart.data(0)
    #print(df1[["CL", "UCL", "LCL"]])
    df2 = chart.data(1)
    #print(df2[["CL", "UCL", "LCL"]])
    #print("stable={0}".format(chart.stable()))
