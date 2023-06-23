"""
Attribute chart: U chart is also known as the control chart for defects per unit chart.

https://sixsigmastudyguide.com/attribute-chart-u-chart/
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
from SPC import UControlChart

if __name__ == '__main__':
    c = np.array([52,48,56,42,39,39,54,56,41,43,47,52,44,47,50,40,47,46,44,50])
    n = np.array([100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100])
    dates = ['21-12-21', '22-12-21', '23-12-21', '24-12-21', '25-12-21', '26-12-21', '27-12-21', '28-12-21', '29-12-21','30-12-21', '31-12-21', '01-01-22', '02-01-22', '03-01-22', '05-01-22', '06-01-22', '07-01-22', '08-01-22', '09-01-22', '10-01-22']
    chart = UControlChart(c=c, n=n, xlabel="x-label", ylabel="y-label")
    chart.dates = dates
    chart.dateformat = "%d-%m-%y"
    #stages=chart.stages(data=chart.value_U, max_stages=2)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([4, 7])
    #chart.limits=True
    chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])
    chart.plot()

    df1 = chart.data(0)
    #print(df1[["CL", "UCL", "LCL"]])
    #print("stable={0}".format(chart.stable()))
