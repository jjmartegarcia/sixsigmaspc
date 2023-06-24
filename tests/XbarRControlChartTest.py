"""
The x-bar and R-chart are control charts used to monitor the mean and variation of a
process based on samples taken in a given time.

X-bar chart: The mean or average change in process over time from subgroup values.
The control limits on the X-Bar brings the sample’s mean and center into consideration.

R-chart: The range of the process over the time from subgroups values.
This monitors the spread of the process over the time.

https://sixsigmastudyguide.com/x-bar-r-control-charts/
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
from SPC import XbarRControlChart

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
    dates = ['21-12-21', '22-12-21', '23-12-21', '24-12-21', '25-12-21', '26-12-21', '27-12-21', '28-12-21', '29-12-21','30-12-21', '31-12-21', '01-01-22', '02-01-22', '03-01-22', '05-01-22', '06-01-22', '07-01-22', '08-01-22', '09-01-22', '10-01-22']
    chart = XbarRControlChart(data=data, xlabel="x-label", ylabel_top="y-label-top", ylabel_bottom="y-label-bottom")
    normally_distributed=chart.normally_distributed(data=chart.value_X, significance_level=0.05)
    print("normally_distributed={0}".format(normally_distributed))
    chart.dates = dates
    chart.dateformat = "%d-%m-%y"
    #stages=chart.stages(data=chart.value_X, max_stages=4)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([5, 11])
    #chart.limits=True
    chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])
    chart.plot()

    df1 = chart.data(0)
    #print(df1[["CL", "UCL", "LCL"]])
    df2 = chart.data(1)
    #print(df2[["CL", "UCL", "LCL"]])
    #print("stable={0}".format(chart.stable()))
