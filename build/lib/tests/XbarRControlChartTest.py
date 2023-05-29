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
    #dates = ['21-12-2021', '22-12-2021', '23-12-2021', '24-12-2021', '25-12-2021', '26-12-2021', '27-12-2021', '28-12-2021', '29-12-2021','30-12-2021', '31-12-2021', '01-01-2022', '02-01-2022', '03-01-2022', '05-01-2022', '06-01-2022', '07-01-2022', '08-01-2022', '09-01-2022', '10-01-2022']
    chart = XbarRControlChart(data=data)
    normally_distributed=chart.normally_distributed(data=chart.value_X, significance_level=0.05)
    print("normally_distributed={0}".format(normally_distributed))
    #chart.dates = dates
    #chart.dateformat = "%d-%m-%Y"
    #stages=chart.stages(data=chart.value_X, max_stages=4)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([5, 11])
    #chart.limits=True
    chart.append_rule(Rule01()) # Beyond limits: one or more points are beyond the control limits.
    chart.append_rule(Rule02()) # Zone A: 2 out of 3 consecutive points in Zone A or beyond.
    chart.append_rule(Rule03()) # Zone B: 4 out of 5 consecutive points in Zone B or beyond.
    chart.append_rule(Rule04()) # Zone C: 7 or more consecutive points on one side of the average (in Zone C or beyond).
    chart.append_rule(Rule05()) # Trend: 7 consecutive points trending up or trending down.
    chart.append_rule(Rule06()) # Mixture: 8 consecutive points with no points in Zone C.
    chart.append_rule(Rule07()) # Stratification: 15 consecutive points in Zone C.
    chart.append_rule(Rule08()) # Over-control: 14 consecutive points alternating up and down.
    chart.plot()

    df1 = chart.data(0)
    print(df1[["CL", "UCL", "LCL"]])
    df2 = chart.data(1)
    print(df2[["CL", "UCL", "LCL"]])
    print("stable={0}".format(chart.stable()))
