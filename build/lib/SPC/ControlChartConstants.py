"""
The abstract class for control chart constants.
"""

from abc import ABC, abstractmethod

class ControlChartConstants(ABC):
    @abstractmethod
    def get_constant(self, n, idx):
        """ Returns the control chart constant.

            :param n: The subgroup size.
            :param idx: The index.
        """
        pass
