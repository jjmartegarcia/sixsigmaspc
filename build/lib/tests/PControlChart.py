"""
Attribute charts: p chart is also known as the control chart for proportions.

https://sixsigmastudyguide.com/p-attribute-charts/
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
from SPC import PControlChart

if __name__ == '__main__':
    c = np.array([18,15,13,16,8,6,18,14,22,12,13,19,33,20,20,20,22,17,19,21])
    n = np.array([1250,1300,1350,1200,1050,1050,1200,1100,1000,600,1350,1250,1200,1100,1050,950,1560,1150,1230,1100])
    #dates = ['21-12-2021', '22-12-2021', '23-12-2021', '24-12-2021', '25-12-2021', '26-12-2021', '27-12-2021', '28-12-2021', '29-12-2021','30-12-2021', '31-12-2021', '01-01-2022', '02-01-2022', '03-01-2022', '05-01-2022', '06-01-2022', '07-01-2022', '08-01-2022', '09-01-2022', '10-01-2022']
    chart = PControlChart(c=c, n=n)
    #chart.dates = dates
    #chart.dateformat = "%d-%m-%Y"
    #stages=chart.stages(data=chart.c, max_stages=2)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([10])
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
    print("stable={0}".format(chart.stable()))
