"""
An individuals and moving range (X-MR) chart is a pair of control charts for processes
with a subgroup size of one. Used to determine if a process is stable and predictable,
it creates a picture of how the system changes over time. The individual (X) chart displays
individual measurements.

https://sixsigmastudyguide.com/xmr-charts/
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
from SPC import XmRControlChart

if __name__ == '__main__':
    data = np.array([2.92, 2.96, 2.86, 3.04, 3.07, 2.85, 3.00, 2.92, 2.97, 2.97, 3.09, 3.07, 2.99, 3.06, 3.05, 3.02, 3.07, 2.91, 3.07, 3.20])
    dates = ['21-12-21', '22-12-21', '23-12-21', '24-12-21', '25-12-21', '26-12-21', '27-12-21', '28-12-21', '29-12-21','30-12-21', '31-12-21', '01-01-22', '02-01-22', '03-01-22', '05-01-22', '06-01-22', '07-01-22', '08-01-22', '09-01-22', '10-01-22']
    chart = XmRControlChart(data=data, xlabel="x-label", ylabel_top="y-label-top", ylabel_bottom="y-label-bottom")
    normally_distributed=chart.normally_distributed(data=chart.value_X, significance_level=0.05)
    print("normally_distributed={0}".format(normally_distributed))
    #chart.dates = dates
    #chart.dateformat = "%d-%m-%y"
    #stages=chart.stages(data=chart.value_X, max_stages=4)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([4, 7])
    #chart.limits=True
    chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])
    chart.plot()

    df1 = chart.data(0)
    #print(df1[["CL", "UCL", "LCL"]])
    df2 = chart.data(1)
    #print(df2[["CL", "UCL", "LCL"]])
    #print("stable={0}".format(chart.stable()))
