"""

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
from SPC import XbarmRControlChart


if __name__ == '__main__':
    data = np.array([[44, 26, 24, 34],
                    [50, 48, 51, 43],
                    [32, 28, 26, 22],
                    [52, 55, 56, 44],
                    [16, 16, 21, 26],
                    [36, 36, 35, 31],
                    [21, 22, 18, 21],
                    [29, 21, 23, 22],
                    [26, 46, 44, 14],
                    [24, 22, 22, 44],
                    [18, 24, 24, 49],
                    [24, 20, 26, 23],
                    [19, 21, 27, 28],
                    [8, 11, 12, 12],
                    [24, 18, 27, 24],
                    [56, 52, 56, 50],
                    [32, 22, 18, 25],
                    [8, 12, 11, 17],
                    [51, 54, 52, 49],
                    [30, 28, 35, 22]])
    #dates = ['21-12-21', '22-12-21', '23-12-21', '24-12-21', '25-12-21', '26-12-21', '27-12-21', '28-12-21', '29-12-21','30-12-21', '31-12-21', '01-01-22', '02-01-22', '03-01-22', '05-01-22', '06-01-22', '07-01-22', '08-01-22', '09-01-22', '10-01-22']
    chart = XbarmRControlChart(data=data, xlabel="x-label", ylabel_top="y-label-top", ylabel_bottom="y-label-bottom")
    #normally_distributed=chart.normally_distributed(significance_level=0.05)
    #print("normally_distributed={0}".format(normally_distributed))
    #chart.dates = dates
    #chart.dateformat = "%d-%m-%y"
    #stages=chart.stages(data=chart.value_X, max_stages=4)
    #if stages is not None:
    #    chart.split(stages)
    #chart.split([4, 7])
    #chart.limits=True
    #chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])
    chart.append_rule(Rule01())
    chart.plot()

    #df1 = chart.data(0)
    #print(df1[["CL", "UCL", "LCL"]])
    #df2 = chart.data(1)
    #print(df2[["CL", "UCL", "LCL"]])
    #print("stable={0}".format(chart.stable()))
    #acorr=chart.auto_correlated(delay=1, threshold=0.7)
    #print("auto_correlated={0}".format(acorr))
