"""
Attribute chart: c chart is also known as the control chart for defects (counting of the number of defects). It is generally used to monitor
the number of defects in constant size units.

https://sixsigmastudyguide.com/attribute-chart-c-chart/
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
from SPC import CControlChart

if __name__ == '__main__':
    c = np.array([12,14,16,18,16,14,12,12,32,16,18,16,14,12,16,18,12,19,18,21])
    n = np.array([500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500])
    dates = ['21-12-21', '22-12-21', '23-12-21', '24-12-21', '25-12-21', '26-12-21', '27-12-21', '28-12-21', '29-12-21','30-12-21', '31-12-21', '01-01-22', '02-01-22', '03-01-22', '05-01-22', '06-01-22', '07-01-22', '08-01-22', '09-01-22', '10-01-22']
    chart = CControlChart(c=c, n=n, xlabel="x-label", ylabel="y-label")
    chart.dates = dates
    chart.dateformat = "%d-%m-%y"
    #stages=chart.stages(data=chart.c, max_stages=2)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([10])
    #chart.limits=True
    chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])
    chart.plot()

    df1 = chart.data(0)
    #print(df1[["CL", "UCL", "LCL"]])
    #print("stable={0}".format(chart.stable()))
