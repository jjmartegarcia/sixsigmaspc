"""
The control chart constants for the X Bar S control chart.
"""

from SPC import ControlChartConstants

class XbarSControlChartConstants(ControlChartConstants):
    def __init__(self):
        self._constants = {
            2: [2.659, 0.7979, 0, 3.267],
            3: [1.954, 0.8862, 0, 2.568],
            4: [1.628, 0.9213, 0, 2.266],
            5: [1.427, 0.94, 0, 2.089],
            6: [1.287, 0.9515, 0.03, 1.970],
            7: [1.182, 0.9594, 0.118, 1.882],
            8: [1.099, 0.9650, 0.185, 1.815],
            9: [1.032, 0.9693, 0.239, 1.761],
            10: [0.975, 0.9727, 0.284, 1.716],
            15: [0.789, 0.9823, 0.428, 1.572],
            25: [0.606, 0.9896, 0.565, 1.435]
            # Add more values as needed n: [A3, c4, B3, B4]
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
    constants = XbarSControlChartConstants()
    A3 = constants.get_constant(4, 0)
    c4 = constants.get_constant(4, 1)
    B3 = constants.get_constant(4, 2)
    B4 = constants.get_constant(4, 3)
    print(A3, c4, B3, B4)
