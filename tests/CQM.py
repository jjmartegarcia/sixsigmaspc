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
from SPC import MultiVariChart
from SPC import ProcessCapabilityChart

if __name__ == '__main__':
    data = np.array([[59, 60], [60, 56], [56, 59], [57, 59], [56, 57], [55, 60], [55, 56], [53, 57], [57, 60], [60, 59], [59, 60], [56, 63], [59, 61], [58, 53], [53, 54], [58, 59], [55, 57], [57, 59], [59, 59], [58, 59], [56, 58], [58, 58], [57, 58], [55, 55], [52, 57], [56, 57], [56, 59], [59, 59], [59, 59], [56, 58], [56, 57], [52, 56], [57, 56], [57, 59], [58, 57], [54, 56], [57, 59], [56, 61], [57, 58], [54, 55], [54, 59], [58, 59], [56, 57], [58, 58], [59, 55], [56, 57], [54, 56], [57, 56], [56, 58], [58, 57], [56, 59], [58, 59], [57, 58], [58, 57], [56, 58], [59, 57], [56, 57], [57, 58], [57, 57], [58, 55], [56, 58], [56, 61], [58, 63], [60, 57], [56, 59], [55, 54], [55, 58], [53, 52], [53, 55], [56, 56], [54, 57], [54, 57], [57, 55], [57, 57], [54, 59], [55, 62], [61, 58], [54, 56], [57, 61], [55, 58], [56, 60], [60, 62], [59, 63], [63, 63], [63, 59], [59, 61], [57, 61], [58, 60], [58, 59], [58, 61], [59, 57], [53, 56], [55, 54], [54, 56], [57, 57], [56, 56], [59, 58], [58, 55], [53, 59], [56, 57], [54, 55], [54, 56], [58, 57], [57, 59], [57, 60], [59, 59], [56, 60], [58, 58], [56, 58], [59, 62], [62, 63], [58, 61], [56, 57], [59, 62], [61, 56], [58, 56], [60, 60], [60, 61], [61, 60], [56, 57], [59, 58], [57, 56], [56, 54], [56, 57], [60, 61], [60, 59], [59, 60], [57, 58], [55, 54], [57, 60], [58, 58], [59, 59], [61, 59], [55, 56], [58, 55], [57, 56], [56, 58], [57, 59], [59, 60], [59, 58], [54, 58], [57, 56], [56, 60], [56, 56], [57, 58], [55, 55], [58, 58], [53, 53], [56, 57], [56, 58], [60, 59], [60, 62], [59, 59], [58, 55], [56, 58], [58, 60], [56, 58], [59, 60], [60, 60], [58, 60], [58, 58], [60, 53], [58, 57], [57, 58], [55, 57], [61, 58], [55, 59], [57, 60], [58, 60], [56, 58], [59, 59]])
    dates = ['01-01-23', '02-01-23', '03-01-23', '04-01-23', '05-01-23', '06-01-23', '07-01-23', '08-01-23', '09-01-23', '10-01-23', '11-01-23', '12-01-23', '13-01-23', '14-01-23', '15-01-23', '16-01-23', '17-01-23', '18-01-23', '19-01-23', '20-01-23', '21-01-23', '22-01-23', '23-01-23', '24-01-23', '25-01-23', '26-01-23', '27-01-23', '28-01-23', '29-01-23', '30-01-23', '31-01-23', '01-02-23', '02-02-23', '03-02-23', '04-02-23', '05-02-23', '06-02-23', '07-02-23', '08-02-23', '09-02-23', '10-02-23', '11-02-23', '12-02-23', '13-02-23', '14-02-23', '15-02-23', '16-02-23', '17-02-23', '18-02-23', '19-02-23', '20-02-23', '21-02-23', '22-02-23', '23-02-23', '24-02-23', '25-02-23', '26-02-23', '27-02-23', '28-02-23', '01-03-23', '02-03-23', '03-03-23', '04-03-23', '05-03-23', '06-03-23', '07-03-23', '08-03-23', '09-03-23', '10-03-23', '11-03-23', '12-03-23', '13-03-23', '14-03-23', '15-03-23', '16-03-23', '17-03-23', '18-03-23', '19-03-23', '20-03-23', '21-03-23', '22-03-23', '23-03-23', '24-03-23', '25-03-23', '26-03-23', '27-03-23', '28-03-23', '29-03-23', '30-03-23', '31-03-23', '01-04-23', '02-04-23', '03-04-23', '04-04-23', '05-04-23', '06-04-23', '07-04-23', '08-04-23', '09-04-23', '10-04-23', '11-04-23', '12-04-23', '13-04-23', '14-04-23', '15-04-23', '16-04-23', '17-04-23', '18-04-23', '19-04-23', '20-04-23', '21-04-23', '22-04-23', '23-04-23', '24-04-23', '25-04-23', '26-04-23', '27-04-23', '28-04-23', '29-04-23', '30-04-23', '01-05-23', '02-05-23', '03-05-23', '04-05-23', '05-05-23', '06-05-23', '07-05-23', '08-05-23', '09-05-23', '10-05-23', '11-05-23', '12-05-23', '13-05-23', '14-05-23', '15-05-23', '16-05-23', '17-05-23', '18-05-23', '19-05-23', '20-05-23', '21-05-23', '22-05-23', '23-05-23', '24-05-23', '25-05-23', '26-05-23', '27-05-23', '28-05-23', '29-05-23', '30-05-23', '31-05-23', '01-06-23', '02-06-23', '03-06-23', '04-06-23', '05-06-23', '06-06-23', '07-06-23', '08-06-23', '09-06-23', '10-06-23', '11-06-23', '12-06-23', '13-06-23', '14-06-23', '15-06-23', '16-06-23', '17-06-23', '18-06-23', '19-06-23', '20-06-23']

    chart = XbarRControlChart(data=data)
    chart.dates = dates
    chart.dateformat = "%d-%m-%y"
    chart.limits = False  # Don't display chart zones.
    chart.append_rule(Rule01())
    chart.plot()

    df1 = chart.data(0)
    print((df1.loc[df1['R01'] == True]).index)
    df2 = chart.data(1)
    print(df2.loc[df2['R01'] == True].index)
    print(dates[11], dates[75], dates[161])

    # Determine the center line and control limits of the X bar.
    df=chart.data(0)
    ucl=round(df['UCL'][0], 2)
    cl=round(df['CL'][0], 2)
    lcl=round(df['LCL'][0], 2)

    normally_distributed = chart.normally_distributed(data=chart.value_X, significance_level=0.05)
    print("normally_distributed={0}".format(normally_distributed))
    print("stable={0}".format(chart.stable()))

    # Perform MultiVariChart analysis
    chart = MultiVariChart(data=data)
    chart.plot()

    # Flatten the data for ProcessCapabilityChart
    data_flat = np.concatenate(data).ravel().tolist()
    
    # Perform ProcessCapabilityChart analysis
    capability = ProcessCapabilityChart(data=data_flat, target=60, LSL=58, USL=70)
    capability.plot(bins=12)

    # Print the analysis results
    print("Cp={0}".format(round(capability.Cp,2)))
    print("Cpk={0}".format(round(capability.Cpk,2)))
    print("mean={0}".format(round(capability.sample_mean,2)))
    print("stdev={0}".format(round(capability.sample_std,2)))
    print("reject_rate={0}%".format(round(capability.reject_rate,2)))

    print("samples={0}".format(capability.num_samples))
    print("max={0}".format(capability.sample_max))
    print("min={0}".format(capability.sample_min))
    print("pct_below_LSL={0}%".format(capability.pct_below_LSL))
    print("pct_above_USL={0}%".format(capability.pct_above_USL))
    print("capable={0}".format(capability.capable(target_cpk=1.33)))
