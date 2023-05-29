"""
An Individual moving range (I-MR) chart is used when data is continuous and not collected in subgroups.
An I-MR chart provides process variation over time in graphical method.
I-MR chart is basically two separate charts – Individuals (I) chart and Moving Range (MR) chart, the combination of two charts provides the complete picture of process behavior.

I-Chart: Individual chart displays the individual data points and monitors mean and shifts in
the process when the data points collected at regular intervals of time. This chart will help to
identify the common and assignable causes in the process, if any.

MR Chart: While Individual chart monitors the process mean, the Moving Range chart monitors the
process variation when the data points collected at regular intervals of time. In other words the
moving range chart tracks the absolute difference of each measurement to its previous measurement.

https://sixsigmastudyguide.com/i-mr-chart/
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
from SPC import ImRControlChart

if __name__ == '__main__':
    data = np.array([82, 84, 75, 79, 84, 81, 81, 82, 80, 78, 74])
    #dates = ['21-12-2021', '22-12-2021', '23-12-2021', '24-12-2021', '25-12-2021', '26-12-2021', '27-12-2021', '28-12-2021', '29-12-2021','30-12-2021', '31-12-2021']
    chart = ImRControlChart(data=data)
    normally_distributed=chart.normally_distributed(data=chart.value_I, significance_level=0.05)
    print("normally_distributed={0}".format(normally_distributed))
    #chart.dates = dates
    #chart.dateformat = "%d-%m-%Y"
    #stages=chart.stages(data=chart.value_I, max_stages=2)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([4, 7])
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
