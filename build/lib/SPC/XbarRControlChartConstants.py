"""
The control chart constants for the X Bar R control chart.
"""

from SPC import ControlChartConstants

class XbarRControlChartConstants(ControlChartConstants):
    def __init__(self):
        self._constants = {
            2: [1.880, 1.128, 0, 3.267],
            3: [1.023, 1.693, 0, 2.574],
            4: [0.729, 2.059, 0, 2.282],
            5: [0.577, 2.326, 0, 2.114],
            6: [0.483, 2.534, 0, 2.004],
            7: [0.419, 2.704, 0.076, 1.924],
            8: [0.373, 2.847, 0.136, 0.1864],
            9: [0.337, 2.970, 0.184, 1.816],
            10: [0.308, 3.078, 0.223, 1.777],
            15: [0.223, 3.472, 0.347, 1.653],
            25: [0.153, 3.931, 0.459, 1.541]
            # Add more values as needed n: [A2, d2, D3, D4]
        }

    def get_constant(self, n, idx):
        """ Returns the control chart constant.

            :param n: The subgroup size.
            :param idx: The index.
        """
        try:
            value= self._constants[n][idx]
            return value
        except KeyError:
            raise ValueError("invalid parameter value(s) for n={0}, idx={1}".format(n, idx))

if __name__ == '__main__':
    constants = XbarRControlChartConstants()
    A2 = constants.get_constant(4, 0)
    d2 = constants.get_constant(4, 1)
    D3 = constants.get_constant(4, 2)
    D4 = constants.get_constant(4, 3)
    print(A2, d2, D3, D4)
